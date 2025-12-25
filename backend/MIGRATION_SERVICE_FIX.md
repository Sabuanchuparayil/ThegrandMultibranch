# Fix: Migration Service Starting Web Server Instead of Running Migrations

## Problem

The migration service is starting Gunicorn (web server) instead of running migrations. This happens because Railway is using the default start command.

## Solution

Use the migration-only script that explicitly runs migrations and exits.

### Step 1: Update Service Start Command

1. Go to Railway dashboard
2. Open your **"run-migrations"** service (or create a new one)
3. Go to **"Settings"** tab
4. Find **"Start Command"** field
5. Replace the current command with:

```bash
bash run_migrations_only.sh
```

**OR** if you prefer Python directly:

```bash
python run_migrations.py
```

### Step 2: Ensure Root Directory is Set

Make sure the service has:
- **Root Directory**: `backend`

### Step 3: Redeploy

1. Go to **"Deployments"** tab
2. Click **"Redeploy"** on the latest deployment
3. Watch the logs - you should see migration output, NOT Gunicorn starting

---

## Expected Log Output (Correct)

```
==================================================================================
RUNNING DATABASE MIGRATIONS (Migration Service)
==================================================================================

Running migration script...
================================================================================
RUNNING DJANGO MIGRATIONS
================================================================================

Step 1: Checking database connection...
✅ Database connection successful

Step 2: Creating migrations for custom apps...
✅ Migrations created (or already exist)

Step 3: Running migrations...
Operations to perform:
  Apply all migrations: ...
Running migrations:
  Applying contenttypes.0001_initial... OK
  ...
✅ All migrations applied successfully

Step 4: Verifying database tables...
✅ 'branches' table exists
✅ 'regions' table exists

================================================================================
✅ Migration process complete!
================================================================================

Exiting migration script. Service can be stopped now.
==================================================================================
✅ Migrations completed successfully!
==================================================================================

This service can now be stopped/deleted.
The database tables have been created.

Waiting 60 seconds for log review, then exiting...
```

---

## What NOT to See (Wrong)

If you see this, the service is still starting Gunicorn:

```
[INFO] Starting gunicorn 23.0.0
[INFO] Listening at: http://0.0.0.0:8080
[INFO] Booting worker with pid: 4
```

This means the start command is wrong - it's using the default web server command instead of the migration script.

---

## Alternative: Use Railway CLI

If the service approach doesn't work, use Railway CLI:

```bash
railway run python run_migrations.py
```

This runs migrations directly without creating a service.

