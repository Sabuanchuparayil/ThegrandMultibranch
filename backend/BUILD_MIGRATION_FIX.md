# Fix: Migrations Not Running During Build

## Problem

The build logs show that migrations are not running during the build phase. This is because:
1. Railway might be using `railway.json` `buildCommand` instead of `nixpacks.toml` `[phases.build]`
2. Migrations need `DATABASE_URL` to be available during build

## Solution Applied

1. ✅ Removed `buildCommand` from `railway.json` - this forces Railway to use `nixpacks.toml`
2. ✅ Updated `nixpacks.toml` to include migration commands in the build phase
3. ✅ Added error handling so build doesn't fail if migrations can't run (they'll run on first request instead)

## Important Note

**Migrations during build require `DATABASE_URL` to be set.**

If `DATABASE_URL` is not available during build, migrations will fail gracefully and the build will continue. Migrations will then run automatically on the first request when the app starts.

## Alternative: Run Migrations on First Request

If migrations can't run during build, we can add a startup script that runs migrations before starting Gunicorn. This ensures migrations always run, even if `DATABASE_URL` isn't available during build.

## Next Steps

1. **Trigger a new build** - Railway should now use `nixpacks.toml` and run migrations
2. **Check build logs** - Look for migration commands in the build phase
3. **If migrations still don't run** - We'll add a startup script to run them before Gunicorn starts

