# Railway Superuser Setup - Quick Guide

## ⚠️ Important Note

**`railway shell` opens a LOCAL subshell with Railway environment variables - it does NOT execute commands on Railway servers.**

To actually run commands on Railway, you MUST use the **Railway Web Shell** (Method 1 below).

## Method 1: Railway Web Shell (REQUIRED - This is the only way)

**You MUST use Railway's web interface to execute commands on the server:**

1. Go to https://railway.app
2. Select your project **"Grand Multibranch"**
3. Click on **backend** service
4. Go to **Deployments** tab
5. Click on the latest deployment
6. Click **Shell** button (opens web terminal - this is different from `railway shell` CLI)
7. Run:
   ```bash
   python manage.py create_auth_token --email mail@jsabu.com --password Admin@1234
   ```
8. Copy the token from the output

**This is the ONLY reliable way to execute commands on Railway servers.**

## Method 2: Railway CLI (Local Only - Won't Work for This)

**Note**: `railway shell` only provides environment variables locally. It does NOT execute commands on Railway servers. Django is not installed locally, so this won't work.

If you want to try locally (requires Django installed):
```bash
python3 manage.py create_auth_token --email mail@jsabu.com --password Admin@1234
```

But this requires:
- Django installed locally
- Database connection to Railway database
- All dependencies installed

**Recommendation**: Use Method 1 (Railway Web Shell) instead.

## What You'll See

```
================================================================================
CREATING ADMIN USER AND AUTH TOKEN
================================================================================
✅ Created admin user: mail@jsabu.com
✅ Added X permissions to user
✅ Created new token for user

================================================================================
AUTHENTICATION TOKEN
================================================================================
Token: [YOUR_TOKEN_HERE]
================================================================================
```

## After Getting the Token

1. **Option A**: Visit `/login` and log in with:
   - Email: `mail@jsabu.com`
   - Password: `Admin@1234`

2. **Option B**: Set token manually in browser console:
   ```javascript
   localStorage.setItem('authToken', 'YOUR_TOKEN_HERE');
   location.reload();
   ```

## Verification

After setting the token:
- Products, Orders, and Customers modules should load without errors
- No more "MANAGE_ORDERS" or "MANAGE_USERS" permission errors
- GraphQL requests will include `Authorization: Bearer <token>` header

