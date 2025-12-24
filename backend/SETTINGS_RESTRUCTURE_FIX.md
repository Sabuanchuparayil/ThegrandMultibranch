# Settings Restructure Fix

## Problem

The deployment fails with:
```
NameError: name 'INSTALLED_APPS' is not defined
```

## Root Cause

When we have a local `saleor/settings/__init__.py` file, Python imports our local module instead of the installed Saleor package's `saleor.settings` module. This creates a circular import issue where we try to import from ourselves.

The complex import manipulation in `__init__.py` was causing the installed Saleor settings to not be imported correctly, leaving `INSTALLED_APPS` undefined.

## Solution

**Simplify by using a different settings module name** that doesn't conflict with Saleor's package structure.

### New Structure

1. **Created `grandgold_settings.py`** (at backend root level):
   - Directly imports from installed `saleor.settings`
   - Extends INSTALLED_APPS and MIDDLEWARE
   - Adds Railway-specific configurations

2. **Updated `wsgi.py`**:
   - Changed `DJANGO_SETTINGS_MODULE` to `'grandgold_settings'`

3. **Updated `manage.py`**:
   - Changed `DJANGO_SETTINGS_MODULE` to `'grandgold_settings'`

4. **Removed conflicting `saleor/settings/` files**:
   - Removed `saleor/settings/__init__.py`
   - Removed `saleor/settings/base.py`
   - Kept `saleor/graphql/` and `saleor/urls.py` (these are our custom files)

### Why This Works

- `grandgold_settings.py` is a standalone module, not part of the `saleor` package
- It can directly import from the installed `saleor.settings` without conflicts
- No circular import issues
- Clean and simple

### Files Changed

- ✅ Created `backend/grandgold_settings.py`
- ✅ Updated `backend/wsgi.py` - uses `grandgold_settings`
- ✅ Updated `backend/manage.py` - uses `grandgold_settings`
- ✅ Removed `backend/saleor/settings/__init__.py`
- ✅ Removed `backend/saleor/settings/base.py`

### Note on `saleor/` Directory

We still keep:
- `saleor/graphql/` - Our custom GraphQL schema extensions
- `saleor/urls.py` - Our URL configuration
- `saleor/__init__.py` - Package marker

But we removed the conflicting `saleor/settings/` directory.

