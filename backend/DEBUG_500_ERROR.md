# Debugging 500 Internal Server Error on GraphQL Endpoint

## Error Observed
When accessing `https://backend-production-d769.up.railway.app/graphql/`, the server returns a 500 Internal Server Error.

## Common Causes

### 1. Database Connection Issues
Saleor requires a database connection. If the database is not accessible, it will cause a 500 error.

**Check:**
- Verify `DATABASE_URL` environment variable is set in Railway
- Check if PostgreSQL service is running
- Verify database credentials are correct
- Check backend logs for database connection errors

**Solution:**
- Ensure PostgreSQL service is deployed and running
- Verify `DATABASE_URL` is correctly set
- Run migrations: `python manage.py migrate`

### 2. Missing Environment Variables
Saleor requires several environment variables. Missing critical ones can cause 500 errors.

**Required Variables:**
- `SECRET_KEY` - Django secret key
- `DATABASE_URL` - PostgreSQL connection string
- `ALLOWED_HOSTS` - Comma-separated list of allowed hosts
- `DJANGO_SETTINGS_MODULE` - Should be `grandgold_settings`

**Check in Railway:**
1. Go to backend service → Variables tab
2. Verify all required variables are set
3. Check for typos in variable names

### 3. Import Errors in Settings
If there's an import error in `grandgold_settings.py`, Django won't start properly.

**Common Issues:**
- Saleor package not installed
- Missing dependencies
- Incorrect import paths
- Circular import issues

**Check:**
- Backend logs for ImportError or ModuleNotFoundError
- Verify Saleor is installed: `pip list | grep saleor`
- Check `requirements.txt` includes all dependencies

### 4. Migration Issues
If database migrations haven't run, tables might be missing, causing 500 errors.

**Solution:**
Run migrations in Railway:
1. Use Railway CLI: `railway run python manage.py migrate`
2. Or add to Procfile/build command

### 5. Saleor Configuration Issues
Saleor might not be properly configured or installed.

**Check:**
- Saleor package is installed correctly
- GraphQL endpoint is properly registered in URLs
- Saleor settings are correctly loaded

## Diagnostic Steps

### Step 1: Check Backend Logs
1. Go to Railway dashboard → Backend service
2. Click "Deployments" → Latest deployment
3. Click "View Logs"
4. Look for:
   - Django startup messages
   - ImportError or ModuleNotFoundError
   - Database connection errors
   - Traceback/stack traces

### Step 2: Check Environment Variables
Verify in Railway backend service → Variables:
- `SECRET_KEY` is set
- `DATABASE_URL` is set (usually auto-created by Railway)
- `DJANGO_SETTINGS_MODULE=grandgold_settings`
- `ALLOWED_HOSTS` includes `*.railway.app` or your domain

### Step 3: Test Database Connection
In Railway CLI or shell:
```bash
railway run python manage.py dbshell
```

If this fails, database connection is the issue.

### Step 4: Check Django Startup
Try to start Django shell:
```bash
railway run python manage.py shell
```

If this fails, there's a configuration or import error.

### Step 5: Run Migrations
```bash
railway run python manage.py migrate
```

Check if migrations run successfully.

### Step 6: Check for Import Errors
Try importing settings:
```bash
railway run python -c "import grandgold_settings; print('Settings loaded successfully')"
```

If this fails, there's an import error in settings.

## Quick Fixes

### Fix 1: Restart Backend Service
1. Railway dashboard → Backend service
2. Click "..." → "Restart"
3. Watch logs for errors during startup

### Fix 2: Verify Requirements
Check `backend/requirements.txt` includes:
- `django>=5.0.0,<6.0`
- `django-cors-headers>=4.2.0`
- Other required dependencies

### Fix 3: Check Procfile
Verify `backend/Procfile` has correct command:
```
web: bash -c 'source .venv/bin/activate && gunicorn wsgi:application --bind 0.0.0.0:$PORT --workers 4 --timeout 120'
```

### Fix 4: Enable Debug Mode Temporarily
Add to Railway environment variables:
```
DEBUG=True
```

This will show detailed error messages instead of generic 500 error.
**Warning:** Only enable in development, disable in production after debugging.

## Expected Backend Logs

When Django starts successfully, you should see logs like:
```
[INFO] Starting gunicorn...
[INFO] Listening at: http://0.0.0.0:PORT
[INFO] Using worker: sync
[INFO] Booting worker with pid: X
[INFO] Django version X.X.X
[INFO] Starting development server at http://0.0.0.0:PORT/
```

## Next Steps

1. **Check Railway Backend Logs** - This will show the actual error causing the 500
2. **Share the error message** from logs so we can identify the specific issue
3. **Verify environment variables** are all set correctly
4. **Check database service** is running and connected

The logs will contain the specific Python traceback showing what's failing. Share those logs for targeted debugging.

