# Auto-Create Superuser on Startup - Complete Guide

## Overview

The backend now automatically creates a superuser and generates an authentication token **on every startup**. This ensures the admin user is always available without needing manual intervention.

## How It Works

1. **On Backend Startup**: When the backend service starts on Railway, it runs:
   - Database migrations
   - Column/table fixes
   - **Superuser creation** (if user doesn't exist)
   - **Token generation** (if token doesn't exist)

2. **Automatic Execution**: The script runs automatically as part of the startup sequence in `grandgold_wsgi.py`

3. **Idempotent**: Safe to run multiple times - it checks if user/token exists before creating

## Default Credentials

- **Email**: `mail@jsabu.com`
- **Password**: `Admin@1234`

## Customizing Credentials

You can override the default credentials using Railway environment variables:

1. Go to Railway dashboard → Backend service → Variables tab
2. Add these variables:
   - `ADMIN_EMAIL=your-email@example.com`
   - `ADMIN_PASSWORD=your-secure-password`
3. Redeploy the service

## Getting the Authentication Token

After the backend starts up, the token will be displayed in the **Railway deployment logs**:

1. Go to Railway dashboard → Backend service
2. Click on "Deployments" tab
3. Click on the latest deployment
4. Click on "Deploy Logs" tab
5. Look for output like:

```
================================================================================
AUTHENTICATION TOKEN
================================================================================
Token: abc123xyz789...
================================================================================
```

## Using the Token

Once you have the token from the logs, use it in one of these ways:

### Option 1: Browser Console (Quick)

1. Open your admin dashboard: `https://admin-dashboard-production-1924.up.railway.app`
2. Open browser DevTools (F12)
3. Go to Console tab
4. Run:
   ```javascript
   localStorage.setItem('authToken', 'YOUR_TOKEN_FROM_LOGS');
   location.reload();
   ```

### Option 2: Environment Variable (Production)

Add to `frontend/admin/.env.local`:
```
NEXT_PUBLIC_AUTH_TOKEN=YOUR_TOKEN_FROM_LOGS
```

Then redeploy the frontend.

### Option 3: Login Page

Visit `/login` and log in with:
- Email: `mail@jsabu.com`
- Password: `Admin@1234`

The token will be automatically stored in localStorage.

## Verification

After setting the token:

1. ✅ Products, Orders, and Customers modules should load without errors
2. ✅ No more "MANAGE_ORDERS" or "MANAGE_USERS" permission errors
3. ✅ GraphQL requests include `Authorization: Bearer <token>` header
4. ✅ Check browser DevTools → Network tab → Request Headers

## Troubleshooting

### Token Not in Logs

If you don't see the token in logs:
1. Check that migrations completed successfully
2. Check for any errors in the "create_superuser_if_needed.py" section
3. The user might already exist - check if you see "Superuser already exists"

### User Already Exists

If the user already exists, the script will:
- Use the existing user
- Generate/retrieve the existing token
- Display it in the logs

### Database Connection Issues

If you see database connection errors:
- The script will skip superuser creation
- It will retry on the next startup
- Ensure your Railway database service is running

## Manual Override

If you need to manually create the superuser (e.g., for testing locally):

```bash
python manage.py create_auth_token --email mail@jsabu.com --password Admin@1234
```

## Files Involved

- `backend/create_superuser_if_needed.py` - Script that creates user and token
- `backend/grandgold_wsgi.py` - Startup sequence that runs the script
- `backend/saleor_extensions/core/management/commands/create_auth_token.py` - Management command (for manual use)

## Next Steps

1. **Wait for deployment**: The changes have been pushed and Railway will automatically deploy
2. **Check logs**: After deployment completes, check the Deploy Logs for the token
3. **Set token**: Use one of the methods above to set the token in your frontend
4. **Test**: Verify that Products, Orders, and Customers modules work without permission errors

