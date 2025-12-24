# Railway Database Migrations Guide

## Quick Start: Run Migrations

### Option 1: Railway CLI (Recommended)

```bash
# 1. Install Railway CLI (if not installed)
npm i -g @railway/cli

# 2. Login to Railway
railway login

# 3. Link to your project (if not already linked)
cd backend
railway link

# 4. Run migrations
railway run python manage.py migrate

# 5. Verify database connection
railway run python verify_and_migrate.py
```

### Option 2: Railway Dashboard

1. Go to your Railway project
2. Click on `backend` service
3. Click **"Deployments"** tab
4. Click on the latest deployment
5. Click **"View Logs"** → Look for **"Shell"** or **"Terminal"** option
6. Run: `python manage.py migrate`

### Option 3: One-Time Migration Service

1. In Railway, click **"+ New"** → **"Empty Service"**
2. Configure:
   - **Name**: `migrations` (temporary)
   - **Root Directory**: `backend`
   - **Start Command**: `python manage.py migrate && sleep 3600`
3. Deploy and wait for migrations to complete
4. Delete the service after migrations are done

## Verify Database Connection

### Check if PostgreSQL is Connected

1. **Railway Dashboard**:
   - Go to your project
   - Check if `Postgres` service shows **"Online"** (green dot)
   - If not, click **"+ New"** → **"Database"** → **"Add PostgreSQL"**

2. **Check Environment Variables**:
   - Go to `backend` service → **"Variables"** tab
   - Look for `DATABASE_URL` (Railway sets this automatically)
   - If missing, PostgreSQL service might not be connected

3. **Test Connection**:
   ```bash
   railway run python verify_and_migrate.py
   ```

## Step-by-Step: First Time Setup

### Step 1: Add PostgreSQL Service

1. In Railway dashboard, click **"+ New"**
2. Select **"Database"** → **"Add PostgreSQL"**
3. Railway will automatically:
   - Create PostgreSQL service
   - Set `DATABASE_URL` environment variable
   - Connect it to your backend service

### Step 2: Verify Connection

```bash
railway run python verify_and_migrate.py
```

Expected output:
```
✅ DATABASE_URL is set
✅ Database connection successful
```

### Step 3: Run Migrations

```bash
railway run python manage.py migrate
```

Expected output:
```
Operations to perform:
  Apply all migrations: ...
Running migrations:
  Applying saleor.0001_initial... OK
  Applying saleor.0002_... OK
  ...
```

### Step 4: Create Superuser (Optional)

```bash
railway run python manage.py createsuperuser
```

Follow prompts to create admin user.

## Troubleshooting

### Error: "DATABASE_URL not set"

**Solution**: 
- Add PostgreSQL service in Railway
- Railway automatically sets `DATABASE_URL`
- Redeploy your backend service

### Error: "could not connect to server"

**Solution**:
- Check if PostgreSQL service is "Online" in Railway
- Wait a few minutes after creating PostgreSQL (takes time to start)
- Check Railway logs for PostgreSQL service

### Error: "relation does not exist"

**Solution**:
- Run migrations: `railway run python manage.py migrate`
- This creates all required database tables

### Error: "No migrations to apply"

**Solution**:
- This is OK! It means all migrations are already applied
- Your database is ready

## Verification Commands

### Check Migration Status

```bash
railway run python manage.py showmigrations
```

### Check Database Tables

```bash
railway run python manage.py dbshell
# Then in PostgreSQL shell:
\dt
# Lists all tables
```

### Test Database Connection

```bash
railway run python -c "from django.db import connection; connection.ensure_connection(); print('✅ Database connected!')"
```

## After Migrations

Once migrations are complete:

1. **Access GraphQL API**: `https://backend-production-d769.up.railway.app/graphql/`
2. **Access Admin Panel**: `https://backend-production-d769.up.railway.app/dashboard/`
3. **Create Superuser**: `railway run python manage.py createsuperuser`

## Important Notes

- **Migrations are one-time**: After running once, you don't need to run again unless you add new models
- **Database persists**: Railway PostgreSQL data persists across deployments
- **Backups**: Railway provides automatic backups on paid plans
- **Connection**: `DATABASE_URL` is automatically set when PostgreSQL service is connected

