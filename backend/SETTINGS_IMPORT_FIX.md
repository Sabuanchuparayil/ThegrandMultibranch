# Settings Import Fix for Railway Deployment

## Problem

Railway deployment fails with:
```
ModuleNotFoundError: No module named 'saleor.settings.base'
```

## Root Cause

When Saleor is installed from GitHub as a package (via `pip install git+https://github.com/saleor/saleor.git`), it provides `saleor.settings` as a **single module**, not a package with `base.py` submodule.

Our local structure has `backend/saleor/settings/base.py`, but when Saleor package is installed, Python finds the installed package first, which only has `saleor.settings` (a module file), not `saleor.settings.base`.

## Solution

### The Fix

1. **Updated `saleor/settings/__init__.py`**:
   - Imports all settings from installed Saleor package: `from saleor.settings import *`
   - Then imports our extensions from `base.py`: `from .base import *`
   - This allows our local `saleor/settings` package to extend the installed Saleor settings

2. **Updated `saleor/settings/base.py`**:
   - Removed direct import of `saleor.settings` 
   - Now only contains extension code (INSTALLED_APPS, MIDDLEWARE, etc.)
   - Settings from Saleor are already imported via `__init__.py`

3. **Updated `wsgi.py` and `manage.py`**:
   - Changed from `saleor.settings.base` to `saleor.settings`
   - This works because our local `saleor/settings` package is in the Python path and extends the installed Saleor settings

### How It Works

```
1. Python imports: saleor.settings
2. Python finds: backend/saleor/settings/__init__.py (our local package)
3. __init__.py imports: from saleor.settings import * (from installed package)
4. __init__.py then imports: from .base import * (our extensions)
5. Result: All Saleor settings + our custom extensions
```

### Files Changed

- ✅ `backend/saleor/settings/__init__.py` - Now properly imports from installed Saleor
- ✅ `backend/saleor/settings/base.py` - Contains only extensions (no Saleor import)
- ✅ `backend/wsgi.py` - Uses `saleor.settings`
- ✅ `backend/manage.py` - Uses `saleor.settings`

## Verification

After deployment, the settings should load correctly because:
1. Our local `saleor/settings` package is in Python path (backend directory)
2. It imports from installed Saleor package
3. It applies our custom extensions
4. Django can find `saleor.settings` module successfully

## Alternative Approach (If Still Failing)

If the above doesn't work, you might need to ensure the backend directory is in Python path. Add to Railway environment variables:

```
PYTHONPATH=/app/backend
```

Or modify `wsgi.py` to explicitly add to path before importing.

