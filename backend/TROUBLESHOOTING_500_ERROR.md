# Troubleshooting 500 Internal Server Error

## Common Causes of 500 Errors

### 1. Database Connection Issues

**Symptom**: 500 error when accessing any URL

**Check**:
- Is PostgreSQL service running in Railway?
- Is `DATABASE_URL` environment variable set?
- Check Railway logs for database connection errors

**Fix**:
1. Ensure PostgreSQL service is added and running
2. Verify `DATABASE_URL` is automatically set (Railway does this)
3. Run migrations: `railway run python manage.py migrate`

### 2. Missing Database Migrations

**Symptom**: 500 error, database-related errors in logs

**Fix**:
```bash
# Via Railway CLI
railway run python manage.py migrate

# Or add to build command temporarily
python manage.py migrate
```

### 3. Missing ROOT_URLCONF

**Symptom**: 500 error, "No URL patterns found" in logs

**Fix**: Already handled in `grandgold_settings.py` - should default to `saleor.urls`

### 4. ALLOWED_HOSTS Configuration

**Symptom**: 400 Bad Request or 500 error

**Fix**: Set in Railway environment variables:
```
ALLOWED_HOSTS=backend-production-d769.up.railway.app,*.railway.app
```

### 5. Missing Environment Variables

**Symptom**: 500 error, specific variable errors in logs

**Required Variables**:
- `SECRET_KEY` (can use temporary for preview)
- `ALLOWED_CLIENT_HOSTS` (defaults to '*' if not set)
- `DATABASE_URL` (auto-provided by Railway PostgreSQL)

## How to Check Railway Logs

### Method 1: Railway Dashboard
1. Go to your Railway project
2. Click on your `backend` service
3. Click **"Logs"** tab
4. Look for error messages (red text)

### Method 2: Railway CLI
```bash
railway logs --service backend
```

### Method 3: Real-time Logs
1. In Railway dashboard → Your service
2. Click **"View Logs"** or **"Deployments"** → Latest deployment
3. Check for Python tracebacks or Django errors

## Quick Diagnostic Steps

1. **Check if service is running**:
   - Railway dashboard → Service status should be "Online" (green)

2. **Check recent deployments**:
   - Railway dashboard → Deployments tab
   - Look for "Deployment successful" (green) or errors (red)

3. **Check application logs**:
   - Look for Python tracebacks
   - Look for Django error messages
   - Look for database connection errors

4. **Test database connection**:
   ```bash
   railway run python manage.py dbshell
   # Or
   railway run python -c "from django.db import connection; connection.ensure_connection(); print('DB OK')"
   ```

5. **Check URL routing**:
   ```bash
   railway run python manage.py show_urls
   ```

## Most Likely Issue: Database Migrations

If you just added PostgreSQL, you need to run migrations:

```bash
# Option 1: Railway CLI
railway run python manage.py migrate

# Option 2: One-time service
# Create a temporary service with start command:
# python manage.py migrate && python manage.py runserver 0.0.0.0:$PORT
```

## Expected URLs After Fix

Once working, you should be able to access:
- **GraphQL API**: `https://backend-production-d769.up.railway.app/graphql/`
- **Admin Panel**: `https://backend-production-d769.up.railway.app/dashboard/`
- **API Root**: `https://backend-production-d769.up.railway.app/`

