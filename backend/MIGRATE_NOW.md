# Run Database Migrations Now

## Quick Method: Railway CLI

### Step 1: Install Railway CLI (if not installed)
```bash
npm i -g @railway/cli
```

### Step 2: Login and Link
```bash
cd backend
railway login
railway link
# Select "Grand Multibranch" or your project name
```

### Step 3: Run Migrations
```bash
railway run python run_migrations.py
```

This will:
- ✅ Check database connection
- ✅ Create migrations for custom apps (branches, regions, inventory, etc.)
- ✅ Run all migrations (Saleor + custom apps)
- ✅ Verify tables are created

---

## Alternative: Railway Dashboard

### Method 1: One-Time Migration Service

1. Go to Railway dashboard: https://railway.app
2. Open your project
3. Click **"+ New"** → **"Empty Service"**
4. Configure:
   - **Name**: `run-migrations` (temporary)
   - **Source**: Same GitHub repo
   - **Root Directory**: `backend`
   - **Start Command**: `python run_migrations.py && echo "Migrations complete!" && sleep 3600`
5. Click **"Deploy"**
6. Wait for deployment and check logs
7. Once migrations are complete, delete this temporary service

### Method 2: Add to Build Process

Migrations are already configured to run automatically during build (see `nixpacks.toml`).

However, if you need to run them manually:

1. Go to your `backend` service in Railway
2. Click **"Deployments"** tab
3. Click **"View Logs"** → Look for **"Shell"** or **"Terminal"**
4. Run: `python run_migrations.py`

---

## Verify Migrations Worked

After running migrations, test the GraphQL endpoint:

```bash
curl -X POST https://backend-production-fb5f.up.railway.app/graphql/ \
  -H "Content-Type: application/json" \
  -d '{"query":"query{branches{ id name code }}"}'
```

You should get data (or an empty array) instead of "relation does not exist" error.

---

## Troubleshooting

### "DATABASE_URL not set"
→ Add PostgreSQL service in Railway dashboard

### "could not connect to server"
→ Wait a few minutes after creating PostgreSQL (takes time to start)

### "No migrations to apply"
→ Good! Database is already set up

### "relation does not exist" (after migrations)
→ Check Railway logs for migration errors
→ Verify PostgreSQL service is connected to backend service

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
  Applying saleor.account.0001_initial... OK
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

