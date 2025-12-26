# How to Run create_auth_token on Railway

## Option 1: Railway Web Interface (Recommended)

1. Go to your Railway project dashboard: https://railway.app
2. Select your **backend** service
3. Click on the **"Deployments"** tab
4. Click on the latest deployment
5. Click on the **"Shell"** button (or use the web terminal)
6. Run the command:
   ```bash
   python manage.py create_auth_token
   ```

## Option 2: Railway CLI (If project is linked)

If your Railway project is linked locally:

```bash
railway run python manage.py create_auth_token
```

## Option 3: Custom Environment Variables

You can also set custom email/password via environment variables:

1. In Railway dashboard, go to your backend service
2. Go to **Variables** tab
3. Add:
   - `ADMIN_EMAIL=your-email@example.com`
   - `ADMIN_PASSWORD=your-secure-password`
4. Then run the command in the shell

## What the Command Does

1. Creates a superuser account (if it doesn't exist)
2. Grants all necessary permissions to the user
3. Generates an authentication token for GraphQL API
4. Displays the token for you to use in the frontend

## Using the Token

After running the command, you'll see a token output. Use it in one of these ways:

### Option A: Frontend Environment Variable
Add to `frontend/admin/.env.local`:
```
NEXT_PUBLIC_AUTH_TOKEN=your-token-here
```

### Option B: Browser Console
Open browser console on admin dashboard and run:
```javascript
localStorage.setItem('authToken', 'your-token-here');
location.reload();
```

### Option C: Update Apollo Client
The Apollo Client is already configured to read from `localStorage.getItem('authToken')`, so just set it as above.

## Troubleshooting

If token generation fails:
- The script will fall back to session-based authentication
- You can log in via Django admin at `/admin/`
- Then use browser cookies for authentication

