# Railway Superuser Setup - Quick Guide

## Method 1: Railway Web Shell (Easiest)

1. Go to https://railway.app
2. Select your project **"Grand Multibranch"**
3. Click on **backend** service
4. Go to **Deployments** tab
5. Click on the latest deployment
6. Click **Shell** button (opens web terminal)
7. Run:
   ```bash
   python manage.py create_auth_token --email mail@jsabu.com --password Admin@1234
   ```
8. Copy the token from the output

## Method 2: Railway CLI (If you have interactive terminal)

If you have an interactive terminal, you can use:

```bash
railway shell
```

Then in the Railway shell:
```bash
python manage.py create_auth_token --email mail@jsabu.com --password Admin@1234
```

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

