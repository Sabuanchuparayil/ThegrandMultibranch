# Run Migrations Now - Step by Step

## Method 1: Railway CLI (Recommended)

### Step 1: Link to Your Railway Project

```bash
cd backend
railway link
```

This will:
- Show a list of your Railway projects
- Ask you to select "Grand Multibranch" or your project name
- Link your local directory to the Railway project

### Step 2: Verify Database Connection

```bash
railway run python verify_and_migrate.py
```

This will:
- Check if `DATABASE_URL` is set
- Test database connection
- Show migration status

### Step 3: Run Migrations

```bash
railway run python manage.py migrate
```

This will:
- Apply all pending migrations
- Create all database tables
- Set up Saleor's database schema

### Step 4: Verify Everything Works

```bash
railway run python manage.py showmigrations --plan
```

Should show all migrations as `[X]` (applied).

---

## Method 2: Railway Dashboard (If CLI doesn't work)

### Step 1: Check PostgreSQL Service

1. Go to Railway dashboard: https://railway.app
2. Open your "Grand Multibranch" project
3. Check if you see a **"Postgres"** service (green "Online" status)
4. If not, click **"+ New"** → **"Database"** → **"Add PostgreSQL"**

### Step 2: Verify DATABASE_URL

1. Click on your `backend` service
2. Go to **"Variables"** tab
3. Look for `DATABASE_URL` (should be automatically set)
4. If missing, PostgreSQL might not be connected

### Step 3: Run Migrations via One-Time Service

1. In Railway, click **"+ New"** → **"Empty Service"**
2. Configure:
   - **Name**: `run-migrations` (temporary)
   - **Source**: Same GitHub repo
   - **Root Directory**: `backend`
   - **Start Command**: `python manage.py migrate && echo "Migrations complete!" && sleep 3600`
3. Click **"Deploy"**
4. Wait for deployment to complete
5. Check logs to see migration output
6. Once done, delete this temporary service

### Step 4: Verify

1. Go back to your `backend` service
2. Check **"Logs"** tab
3. Access your URL: `https://backend-production-d769.up.railway.app`
4. Should no longer show 500 error

---

## Method 3: Add Migrations to Build Process

If you want migrations to run automatically on each deployment:

1. Edit `backend/nixpacks.toml`
2. Add to `[phases.build]` section:

```toml
[phases.build]
cmds = [
  ". .venv/bin/activate && python manage.py collectstatic --noinput || true",
  ". .venv/bin/activate && python manage.py migrate --noinput || true",
]
```

**Note**: This runs migrations on every deployment. Usually you only need to run them once.

---

## Quick Checklist

- [ ] PostgreSQL service exists and is "Online" in Railway
- [ ] `DATABASE_URL` is set in backend service variables
- [ ] Migrations have been run (check logs)
- [ ] Application URL no longer shows 500 error

---

## Expected Output

When migrations run successfully, you'll see:

```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions, saleor, ...
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying saleor.account.0001_initial... OK
  Applying saleor.order.0001_initial... OK
  ... (many more)
```

---

## After Migrations Complete

1. **Test the application**: Visit `https://backend-production-d769.up.railway.app/graphql/`
2. **Create admin user** (optional):
   ```bash
   railway run python manage.py createsuperuser
   ```
3. **Access admin panel**: `https://backend-production-d769.up.railway.app/dashboard/`

---

## If You Get Errors

### "DATABASE_URL not set"
→ Add PostgreSQL service in Railway

### "could not connect to server"
→ Wait a few minutes after creating PostgreSQL (takes time to start)

### "relation does not exist"
→ Migrations haven't been run yet - run them now!

### "No migrations to apply"
→ Good! Database is already set up


