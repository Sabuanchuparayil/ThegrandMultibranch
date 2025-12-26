# Railway Deployment Fix - Saleor Installation

## Problem

Railway deployment fails with:
```
ERROR: Could not find a version that satisfies the requirement saleor>=3.20.0 (from versions: none)
```

## Root Cause

Saleor is **not available on PyPI**. It must be installed from GitHub repository.

## Solution

Three options to fix this:

### Option 1: Use Nixpacks Configuration (Recommended)

Railway uses Nixpacks by default. Create `nixpacks.toml` in the `backend/` directory:

```toml
[phases.setup]
nixPkgs = ["python311", "git"]

[phases.install]
cmds = [
  "pip install --upgrade pip setuptools wheel",
  "pip install -r requirements.txt",
  "pip install git+https://github.com/saleor/saleor.git",
]

[phases.build]
cmds = [
  "python manage.py collectstatic --noinput || true",
]

[start]
cmd = "gunicorn saleor.wsgi:application --bind 0.0.0.0:$PORT --workers 4 --timeout 120"
```

### Option 2: Use Railway.json Build Command

Create `railway.json` in `backend/` directory:

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "pip install --upgrade pip && pip install -r requirements.txt && pip install git+https://github.com/saleor/saleor.git"
  },
  "deploy": {
    "startCommand": "gunicorn saleor.wsgi:application --bind 0.0.0.0:$PORT --workers 4 --timeout 120"
  }
}
```

### Option 3: Update requirements.txt (Simpler)

**Current requirements.txt should NOT include Saleor line**, as it's not on PyPI.

The requirements.txt should contain all dependencies EXCEPT Saleor:

```txt
# Saleor is installed separately from GitHub
django>=4.2.0,<5.0
psycopg2-binary>=2.9.0
redis>=5.0.0
celery>=5.3.0
...
```

Then configure Railway service to run:
```
Build Command: pip install -r requirements.txt && pip install git+https://github.com/saleor/saleor.git
```

## Steps to Fix

1. **Remove Saleor from requirements.txt** (if present)
2. **Create nixpacks.toml** with the configuration above
3. **Commit and push** the changes
4. **Redeploy** on Railway

## Files to Update

- ✅ `backend/requirements.txt` - Remove `saleor>=3.20.0` line
- ✅ `backend/nixpacks.toml` - Add Nixpacks configuration (already created)
- ✅ Commit and push changes

## Verification

After deployment, check logs to ensure:
- ✅ Saleor installs successfully from GitHub
- ✅ All dependencies install correctly
- ✅ Application starts without errors

## Alternative: Use Dockerfile

If Nixpacks doesn't work, you can use a Dockerfile instead:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install git+https://github.com/saleor/saleor.git

# Copy application code
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput || true

# Run gunicorn
CMD gunicorn saleor.wsgi:application --bind 0.0.0.0:$PORT --workers 4 --timeout 120
```

Then in Railway, select "Dockerfile" as the builder.


