# 🚂 Railway Setup & GitHub Configuration Guide

Complete guide for setting up Railway deployment and GitHub repository for Grand Gold & Diamonds platform.

---

## 📋 Table of Contents

1. [GitHub Repository Setup](#github-repository-setup)
2. [Railway Account Setup](#railway-account-setup)
3. [Backend Services Deployment](#backend-services-deployment)
4. [Environment Variables Configuration](#environment-variables-configuration)
5. [Database & Redis Setup](#database--redis-setup)
6. [Frontend Deployment (Optional)](#frontend-deployment-optional)
7. [Domain Configuration](#domain-configuration)
8. [Monitoring & Logs](#monitoring--logs)

---

## 🔷 GitHub Repository Setup

### Step 1: Create GitHub Repository

1. Go to [GitHub](https://github.com) and sign in
2. Click **"New repository"** (or go to https://github.com/new)
3. Fill in repository details:
   ```
   Repository name: grand-gold-multibranch
   Description: Multi-branch jewellery e-commerce platform with Saleor backend
   Visibility: Private (recommended) or Public
   Initialize with: README, .gitignore (Node), License (optional)
   ```
4. Click **"Create repository"**

### Step 2: Initialize Local Git Repository

```bash
cd "/Users/apple/Desktop/Grand Gold/The grand-Multibranch"

# Initialize git if not already done
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Multi-branch jewellery platform"

# Add remote repository
git remote add origin https://github.com/YOUR_USERNAME/grand-gold-multibranch.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 3: Repository Structure

Your repository should have this structure:

```
grand-gold-multibranch/
├── backend/                 # Django/Saleor backend
│   ├── saleor/
│   ├── saleor_extensions/
│   ├── manage.py
│   ├── requirements.txt
│   ├── Procfile
│   ├── runtime.txt
│   └── .env.example
├── frontend/
│   ├── admin/              # Admin dashboard
│   ├── storefront/         # Customer storefront
│   └── shared/             # Shared types
├── docs/                   # Documentation
└── README.md
```

### Step 4: GitHub Secrets (For CI/CD - Optional)

If you want to set up GitHub Actions for CI/CD:

1. Go to repository **Settings** → **Secrets and variables** → **Actions**
2. Add the following secrets:
   - `RAILWAY_TOKEN` - Railway API token
   - `DATABASE_URL` - Production database URL
   - `SECRET_KEY` - Django secret key

---

## 🚂 Railway Account Setup

### Step 1: Create Railway Account

1. Go to [Railway](https://railway.app)
2. Click **"Start a New Project"**
3. Sign up with GitHub (recommended) or email
4. Authorize Railway to access your GitHub account

### Step 2: Create Railway Project

1. In Railway dashboard, click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose your repository: `grand-gold-multibranch`
4. Railway will create a new project

---

## 🔧 Backend Services Deployment

### Step 1: Add PostgreSQL Database

1. In Railway project, click **"+ New"**
2. Select **"Database"** → **"Add PostgreSQL"**
3. Railway will automatically:
   - Create PostgreSQL database
   - Generate `DATABASE_URL` environment variable
   - Add to all services

**Note the connection details** (you'll need them for local development)

### Step 2: Add Redis Service

1. Click **"+ New"**
2. Select **"Database"** → **"Add Redis"**
3. Railway will create Redis and add `REDIS_URL` environment variable

### Step 3: Deploy Backend API Service

1. Click **"+ New"**
2. Select **"GitHub Repo"**
3. Choose your repository
4. Configure the service:
   - **Name**: `backend-api`
   - **Root Directory**: `backend`
   - **Start Command**: Leave empty (uses Procfile)
   - **Build Command**: `pip install -r requirements.txt`

Railway will auto-detect Python and use the `Procfile`.

### Step 4: Deploy Celery Worker

1. Click **"+ New"** → **"GitHub Repo"**
2. Choose the same repository
3. Configure:
   - **Name**: `celery-worker`
   - **Root Directory**: `backend`
   - **Start Command**: `celery -A saleor worker -l info --concurrency=4`
   - Copy environment variables from `backend-api` service

### Step 5: Deploy Celery Beat

1. Click **"+ New"** → **"GitHub Repo"**
2. Choose the same repository
3. Configure:
   - **Name**: `celery-beat`
   - **Root Directory**: `backend`
   - **Start Command**: `celery -A saleor beat -l info`
   - Copy environment variables from `backend-api` service

---

## ⚙️ Environment Variables Configuration

### Required Environment Variables

Configure these in Railway for each service (or use shared variables):

#### For All Backend Services:

```bash
# Django Settings
SECRET_KEY=your-super-secret-key-here-generate-with-python
DEBUG=False
ALLOWED_HOSTS=your-app.railway.app,your-custom-domain.com

# Database (Auto-created by Railway - DON'T override)
# DATABASE_URL is automatically set by Railway

# Redis (Auto-created by Railway - DON'T override)
# REDIS_URL is automatically set by Railway

# AWS S3 (Required for media files)
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_STORAGE_BUCKET_NAME=grand-gold-media
AWS_S3_REGION_NAME=us-east-1
AWS_S3_CUSTOM_DOMAIN=grand-gold-media.s3.amazonaws.com

# Email Configuration
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=your-sendgrid-api-key
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=noreply@grandgold.com

# Currency & Gold Rate APIs
CURRENCY_API_KEY=your-currency-api-key
GOLD_RATE_API_KEY_UK=your-uk-gold-api-key
GOLD_RATE_API_KEY_UAE=your-uae-gold-api-key
GOLD_RATE_API_KEY_INDIA=your-india-gold-api-key

# Payment Gateways - UK (Stripe)
STRIPE_PUBLIC_KEY=your-stripe-public-key
STRIPE_SECRET_KEY=your-stripe-secret-key
STRIPE_WEBHOOK_SECRET=your-stripe-webhook-secret

# Payment Gateways - India (Razorpay)
RAZORPAY_KEY_ID=your-razorpay-key-id
RAZORPAY_KEY_SECRET=your-razorpay-key-secret

# Payment Gateways - UAE (PayTabs)
PAYTABS_PROFILE_ID=your-paytabs-profile-id
PAYTABS_SERVER_KEY=your-paytabs-server-key

# Sentry (Error Tracking)
SENTRY_DSN=your-sentry-dsn
SENTRY_ENVIRONMENT=production

# CORS
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com,https://admin.your-domain.com

# Saleor Specific
ALLOWED_GRAPHQL_ORIGINS=*
ALLOWED_HOSTS=your-app.railway.app,your-custom-domain.com
```

### How to Set Environment Variables in Railway

#### Method 1: Per Service (Individual)

1. Click on a service (e.g., `backend-api`)
2. Go to **"Variables"** tab
3. Click **"+ New Variable"**
4. Add each variable name and value
5. Click **"Add"**

#### Method 2: Shared Variables (Recommended)

1. Go to project settings (click project name)
2. Go to **"Variables"** tab
3. Click **"+ New Variable"**
4. Variables here are shared across all services
5. Mark as **"Shared"** if needed

#### Method 3: Using Railway CLI

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Link to project
railway link

# Set variables
railway variables set SECRET_KEY=your-secret-key
railway variables set AWS_ACCESS_KEY_ID=your-key
# etc.
```

### Generate Secret Key

```bash
# Generate a secure secret key
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

---

## 🗄️ Database & Redis Setup

### PostgreSQL Configuration

Railway automatically provides:
- Database URL in format: `postgresql://user:password@host:port/dbname`
- Connection pooling
- Automatic backups (on paid plans)

### Redis Configuration

Railway automatically provides:
- Redis URL in format: `redis://default:password@host:port`
- Persistent storage option

### Running Migrations

After deployment, run migrations:

**Option 1: Via Railway CLI**

```bash
railway run python manage.py migrate
```

**Option 2: Via Railway Dashboard**

1. Go to `backend-api` service
2. Click **"Deployments"** → Latest deployment
3. Click **"View Logs"** → **"Shell"** (if available)
4. Or create a one-off command via CLI

**Option 3: Create Migration Service (One-time)**

Temporarily add a service that runs migrations on startup:

1. Add new service with:
   - **Start Command**: `python manage.py migrate && python manage.py collectstatic --noinput`
   - Delete after migrations complete

---

## 🌐 Frontend Deployment (Optional)

### Option 1: Deploy to Railway

1. Click **"+ New"** → **"GitHub Repo"**
2. Select repository
3. Configure:
   - **Root Directory**: `frontend/admin` (for admin) or `frontend/storefront` (for storefront)
   - **Build Command**: `npm install && npm run build`
   - **Start Command**: `npm start`
   - **Environment Variables**:
     ```
     NEXT_PUBLIC_API_URL=https://your-backend.railway.app
     NEXT_PUBLIC_GRAPHQL_URL=https://your-backend.railway.app/graphql/
     ```

### Option 2: Deploy to Vercel (Recommended for Next.js)

1. Go to [Vercel](https://vercel.com)
2. Import your GitHub repository
3. Configure:
   - **Framework Preset**: Next.js
   - **Root Directory**: `frontend/admin` or `frontend/storefront`
   - **Environment Variables**: Same as above

---

## 🔐 Domain Configuration

### Step 1: Get Railway Domain

1. Go to your `backend-api` service
2. Click **"Settings"** → **"Domains"**
3. Railway provides: `your-app.up.railway.app`
4. Note this URL

### Step 2: Custom Domain (Optional)

1. In **"Domains"** section, click **"Custom Domain"**
2. Enter your domain: `api.yourdomain.com`
3. Railway will provide DNS records to add:
   ```
   Type: CNAME
   Name: api
   Value: your-app.up.railway.app
   ```
4. Add this record in your domain registrar (GoDaddy, Namecheap, etc.)
5. Wait for DNS propagation (can take up to 48 hours)

### Step 3: Update Environment Variables

After domain is set:
1. Update `ALLOWED_HOSTS`:
   ```
   ALLOWED_HOSTS=api.yourdomain.com,your-app.railway.app
   ```
2. Update `CORS_ALLOWED_ORIGINS`:
   ```
   CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://admin.yourdomain.com
   ```

---

## 📊 Monitoring & Logs

### View Logs

1. Go to any service in Railway
2. Click **"Deployments"** → Select deployment
3. Click **"View Logs"**
4. Filter by service type

### Metrics

Railway provides:
- CPU usage
- Memory usage
- Network traffic
- Request logs

### Health Checks

Railway automatically checks:
- Service availability
- Port binding
- Startup success

---

## 🔄 Continuous Deployment

Railway automatically deploys when you push to GitHub:

1. Push changes to GitHub:
   ```bash
   git add .
   git commit -m "Your changes"
   git push origin main
   ```

2. Railway detects changes
3. Builds and deploys automatically
4. Shows deployment status in dashboard

### Branch Deployments (Optional)

1. Go to service settings
2. Enable **"Branch Deployments"**
3. Railway will create deployments for each branch
4. Useful for staging/testing

---

## 📝 Railway Service Configuration Summary

| Service | Type | Start Command | Root Dir |
|---------|------|---------------|----------|
| backend-api | Web | (from Procfile) | `backend` |
| celery-worker | Worker | `celery -A saleor worker -l info` | `backend` |
| celery-beat | Worker | `celery -A saleor beat -l info` | `backend` |
| postgresql | Database | (managed) | - |
| redis | Database | (managed) | - |

---

## 🔍 Verification Steps

### 1. Check Backend API

```bash
# Test GraphQL endpoint
curl https://your-app.railway.app/graphql/ \
  -X POST \
  -H "Content-Type: application/json" \
  -d '{"query": "{ __schema { queryType { name } } }"}'
```

### 2. Check Database Connection

View logs in Railway to confirm database connection.

### 3. Check Redis Connection

Check Celery worker logs to confirm Redis connection.

---

## 🚨 Common Issues & Solutions

### Issue: Build Fails

**Solution:**
- Check `requirements.txt` is correct
- Verify Python version in `runtime.txt`
- Check build logs in Railway

### Issue: Database Connection Error

**Solution:**
- Verify `DATABASE_URL` is set correctly
- Check database service is running
- Verify network connectivity

### Issue: Static Files Not Serving

**Solution:**
- Run `collectstatic` during build
- Configure AWS S3 for media files
- Check `STATIC_URL` setting

### Issue: Environment Variables Not Loading

**Solution:**
- Restart services after adding variables
- Check variable names match exactly
- Verify variables are shared if needed

---

## 📚 Additional Resources

- [Railway Documentation](https://docs.railway.app)
- [Railway CLI Documentation](https://docs.railway.app/develop/cli)
- [Saleor Documentation](https://docs.saleor.io)
- [Next.js Deployment](https://nextjs.org/docs/deployment)

---

## ✅ Checklist

Before going live:

- [ ] GitHub repository created and pushed
- [ ] Railway account created
- [ ] PostgreSQL database added
- [ ] Redis service added
- [ ] Backend API deployed
- [ ] Celery worker deployed
- [ ] Celery beat deployed
- [ ] All environment variables configured
- [ ] Migrations run successfully
- [ ] AWS S3 configured
- [ ] Domain configured (optional)
- [ ] Health checks passing
- [ ] Logs reviewed
- [ ] Frontend deployed (optional)

---

**Status**: Ready for Railway deployment! 🚀


