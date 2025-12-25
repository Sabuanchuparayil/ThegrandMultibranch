# Auto-Migration Setup

## ✅ Migrations are Already Configured!

Migrations are configured to run **automatically during every build** in `nixpacks.toml`.

## How It Works

When Railway builds your backend service, it will:
1. ✅ Install dependencies
2. ✅ Run `makemigrations` for custom apps
3. ✅ Run `migrate` to create all database tables
4. ✅ Then start the web server

## To Run Migrations Now

### Option 1: Trigger a Redeploy (Recommended)

1. Go to Railway dashboard
2. Open your **backend** service (NOT the migration service)
3. Go to **"Deployments"** tab
4. Click **"Redeploy"** on the latest deployment
5. Watch the build logs - you'll see migrations running during the build phase

### Option 2: Push a Small Change

Make a small change to trigger a rebuild:

```bash
# Add a comment to trigger rebuild
echo "# Auto-migration enabled" >> backend/nixpacks.toml
git add backend/nixpacks.toml
git commit -m "Trigger rebuild for auto-migration"
git push origin main
```

Railway will automatically:
- Build the service
- Run migrations during build
- Deploy the service

## What to Look For in Build Logs

During the build phase, you should see:

```
[phases.build] Running commands...
[phases.build] . .venv/bin/activate && python manage.py makemigrations ...
Migrations for 'regions':
  saleor_extensions/regions/migrations/0001_initial.py
    - Create model Region
...
[phases.build] . .venv/bin/activate && python manage.py migrate ...
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, saleor, ...
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
  Applying saleor_extensions.regions.0001_initial... OK
  Applying saleor_extensions.branches.0001_initial... OK
  Applying saleor_extensions.inventory.0001_initial... OK
```

## After Migrations Complete

Once the build completes:
1. ✅ All database tables will be created
2. ✅ The backend service will start normally
3. ✅ GraphQL queries will work (no more "relation does not exist" errors)

## Delete the Migration Service

Since migrations run automatically during build, you can delete the separate migration service:

1. Go to Railway dashboard
2. Find the **"run-migrations"** service (or whatever you named it)
3. Click the **"..."** menu → **"Delete"**
4. Confirm deletion

You don't need it anymore - migrations run automatically!

---

## Troubleshooting

### Migrations Not Running During Build

If you don't see migrations in the build logs:
1. Check that `nixpacks.toml` exists in the `backend/` directory
2. Verify the build commands are correct
3. Check Railway is using Nixpacks (not Dockerfile)

### "No migrations to apply"

This is OK! It means migrations have already been run. Your database is up to date.

### "Migration failed"

Check:
- Database connection (DATABASE_URL is set)
- PostgreSQL service is running
- Build logs for specific error messages

