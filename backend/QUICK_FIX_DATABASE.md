# Quick Fix: Database Migration Error

## Current Error
```
relation "branches" does not exist
```

## Solution: Run Database Migrations

The database tables haven't been created yet. Run migrations using one of these methods:

### Method 1: Railway CLI (Fastest)

```bash
# 1. Install Railway CLI (if not installed)
npm i -g @railway/cli

# 2. Login and link
cd backend
railway login
railway link

# 3. Run migrations
railway run python run_migrations.py
```

### Method 2: Railway Dashboard

1. Go to Railway dashboard: https://railway.app
2. Open your **backend** service
3. Click **"Deployments"** tab
4. Click on the latest deployment
5. Click **"View Logs"** → Look for **"Shell"** or **"Terminal"** button
6. Run: `python run_migrations.py`

### Method 3: One-Time Migration Service

1. In Railway, click **"+ New"** → **"Empty Service"**
2. Configure:
   - **Name**: `run-migrations` (temporary)
   - **Source**: Same GitHub repo
   - **Root Directory**: `backend`
   - **Start Command**: `python run_migrations.py && echo "Migrations complete!" && sleep 3600`
3. Click **"Deploy"**
4. Wait for migrations to complete (check logs)
5. Delete this temporary service after migrations are done

---

## What This Does

The migration script will:
1. ✅ Check database connection
2. ✅ Create migration files for custom apps (branches, regions, inventory, etc.)
3. ✅ Run all migrations (Saleor + custom apps)
4. ✅ Create all database tables
5. ✅ Verify tables exist

---

## After Migrations Complete

Once migrations are done, refresh the admin dashboard. The error should be gone and you should see:
- ✅ No more "relation does not exist" errors
- ✅ GraphQL queries returning data (or empty arrays if no data yet)
- ✅ Ability to create branches, regions, etc.

---

## Expected Output

When migrations run successfully, you'll see:

```
================================================================================
RUNNING DJANGO MIGRATIONS
================================================================================

Step 1: Checking database connection...
✅ Database connection successful

Step 2: Creating migrations for custom apps...
✅ Migrations created (or already exist)

Step 3: Running migrations...
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, saleor, ...
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
  Applying saleor_extensions.regions.0001_initial... OK
  Applying saleor_extensions.branches.0001_initial... OK
  Applying saleor_extensions.inventory.0001_initial... OK
✅ All migrations applied successfully

Step 4: Verifying database tables...
✅ 'branches' table exists
✅ 'regions' table exists

================================================================================
✅ Migration process complete!
================================================================================
```

---

## Troubleshooting

### "DATABASE_URL not set"
→ Add PostgreSQL service in Railway dashboard

### "could not connect to server"
→ Wait a few minutes after creating PostgreSQL (takes time to start)

### "No migrations to apply"
→ Good! Database is already set up

