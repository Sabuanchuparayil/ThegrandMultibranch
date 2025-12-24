# WSGI Configuration Fix

## Problem

Railway deployment fails with:
```
ModuleNotFoundError: No module named 'saleor.wsgi'
```

## Root Cause

When Saleor is installed from GitHub as a package, it doesn't include a `wsgi.py` file in the `saleor` package. We need to create our own WSGI file that references our custom settings.

## Solution

### Option 1: Use Local WSGI File (Implemented)

Created `backend/wsgi.py` that:
1. Sets the Django settings module to `saleor.settings.base`
2. Uses Django's `get_wsgi_application()` to create the WSGI app
3. Can be directly referenced by Gunicorn

**Procfile updated to:**
```
web: gunicorn wsgi:application --bind 0.0.0.0:$PORT --workers 4 --timeout 120
```

### Option 2: Use Saleor's Built-in WSGI (If Available)

If Saleor package has a WSGI, you could try:
```
web: gunicorn saleor.core.wsgi:application --bind 0.0.0.0:$PORT --workers 4 --timeout 120
```

But this is less reliable as it depends on Saleor's package structure.

## Files Created/Modified

1. ✅ `backend/wsgi.py` - WSGI application file
2. ✅ `backend/Procfile` - Updated to use `wsgi:application`
3. ✅ `backend/nixpacks.toml` - Updated start command
4. ✅ `backend/saleor/__init__.py` - Package initialization

## Verification

The WSGI file:
- Uses `saleor.settings.base` as the settings module
- Creates Django WSGI application
- Should work with Gunicorn

## Next Steps

1. Commit and push changes
2. Redeploy on Railway
3. Verify the application starts successfully

