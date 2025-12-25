# Migration Alternatives

Since migrations are failing during deployment, here are alternative approaches:

## Option 1: Generate Migrations Locally (Recommended)

**Best for**: Development workflow where you can run migrations locally first

### Steps:
1. **Generate migrations locally** (on your machine):
   ```bash
   cd backend
   source .venv/bin/activate  # or your virtual environment
   python manage.py makemigrations regions currency branches inventory
   ```

2. **Test migrations locally**:
   ```bash
   python manage.py migrate
   ```

3. **Commit migration files** to git:
   ```bash
   git add saleor_extensions/*/migrations/
   git commit -m "Add migration files"
   git push
   ```

4. **On Railway, only run `migrate`** (not `makemigrations`):
   - Update `nixpacks.toml` to remove `makemigrations` command
   - Only run `migrate` during build or startup

### Benefits:
- ✅ Avoids all import issues during `makemigrations` on Railway
- ✅ Migrations are tested locally first
- ✅ Faster deployments (no migration generation)
- ✅ More predictable

---

## Option 2: Separate Migration Service

**Best for**: Production environments where you want to control when migrations run

### Steps:
1. **Create a separate Railway service** called "migrations" or "run-migrations"
2. **Set the start command** to:
   ```bash
   bash -c 'LIB_PATH=$(find /nix/store -name libmagic.so* 2>/dev/null | head -1 | xargs dirname 2>/dev/null); export LD_LIBRARY_PATH=$LD_LIBRARY_PATH${LIB_PATH:+:$LIB_PATH} && source .venv/bin/activate && python manage.py migrate --noinput'
   ```
3. **Run this service manually** when you need to migrate
4. **Main app service** doesn't run migrations at all

### Benefits:
- ✅ Complete control over when migrations run
- ✅ Can test migrations before deploying main app
- ✅ Main app doesn't fail if migrations have issues
- ✅ Can run migrations during maintenance windows

---

## Option 3: SQL Scripts (Manual Table Creation)

**Best for**: Simple schemas or when you want full control

### Steps:
1. **Create SQL scripts** for each app:
   ```sql
   -- backend/sql/create_branches_tables.sql
   CREATE TABLE IF NOT EXISTS branches (
       id SERIAL PRIMARY KEY,
       name VARCHAR(255) NOT NULL,
       code VARCHAR(100) UNIQUE NOT NULL,
       -- ... other fields
   );
   ```

2. **Run SQL directly** on Railway database:
   - Use Railway's database console
   - Or use a one-time service that runs the SQL

### Benefits:
- ✅ Complete control
- ✅ No Django migration system dependencies
- ✅ Can be version controlled

### Drawbacks:
- ❌ Manual work
- ❌ No automatic migration tracking
- ❌ Harder to rollback

---

## Option 4: Disable Auto-Migrations, Run Manually

**Best for**: When you want to migrate only when needed

### Steps:
1. **Remove all migration commands** from `nixpacks.toml` and `grandgold_wsgi.py`
2. **Run migrations manually** via Railway CLI:
   ```bash
   railway run python manage.py migrate
   ```

### Benefits:
- ✅ No automatic failures
- ✅ Full control
- ✅ Can test before applying

---

## Recommended Approach

**I recommend Option 1** (Generate migrations locally):

1. It's the most Django-idiomatic approach
2. Migrations are tested before deployment
3. Avoids all the import issues we've been having
4. Faster deployments

Would you like me to:
1. Update `nixpacks.toml` to remove `makemigrations` and only run `migrate`?
2. Create a script to help you generate migrations locally?
3. Set up Option 2 (separate migration service)?

