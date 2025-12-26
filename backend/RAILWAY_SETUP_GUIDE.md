# 🚂 Railway Deployment Setup Guide

Complete step-by-step guide for deploying the Grand Gold & Diamonds multi-branch jewellery platform to Railway.

## 📋 Prerequisites

Before starting, ensure you have:

1. ✅ **GitHub Account** - For repository hosting
2. ✅ **Railway Account** - Sign up at [railway.app](https://railway.app)
3. ✅ **AWS Account** (optional) - For S3 media storage
4. ✅ **Git Repository** - Your code pushed to GitHub

## 🚀 Step 1: Prepare Your Repository

### 1.1 Ensure All Files Are Committed

```bash
cd "/Users/apple/Desktop/Grand Gold/The grand-Multibranch"

# Check git status
git status

# Add all files
git add .

# Commit if needed
git commit -m "Complete backend implementation with GraphQL APIs"

# Push to GitHub
git push origin main
```

### 1.2 Verify Important Files

Ensure these files exist in your repository:

```
backend/
├── manage.py                    ✅ Required
├── Procfile                     ✅ Required for Railway
├── runtime.txt                  ✅ Required (Python version)
├── requirements.txt             ✅ Required
├── saleor/
│   └── settings/
│       ├── __init__.py          ✅ Required
│       ├── base.py              ✅ Required
│       └── local.py.example     ✅ Reference
└── saleor_extensions/           ✅ All apps
```

## 🔧 Step 2: Create Railway Account & Project

### 2.1 Sign Up/Login

1. Go to [railway.app](https://railway.app)
2. Click **"Login"** or **"Start a New Project"**
3. Sign in with your GitHub account (recommended)

### 2.2 Create New Project

1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose your repository: `The grand-Multibranch`
4. Railway will create a new project

## 🗄️ Step 3: Add Database Service (PostgreSQL)

### 3.1 Add PostgreSQL

1. In your Railway project dashboard, click **"+ New"**
2. Select **"Database"** → **"Add PostgreSQL"**
3. Railway will automatically:
   - Create a PostgreSQL database
   - Generate `DATABASE_URL` environment variable
   - Provision the database service

### 3.2 Note Database Connection

The `DATABASE_URL` is automatically created. You'll use it in your API service settings.

**Format**: `postgresql://postgres:PASSWORD@HOST:PORT/railway`

## 📦 Step 4: Add Redis Service

### 4.1 Add Redis

1. Click **"+ New"**
2. Select **"Database"** → **"Add Redis"**
3. Railway will automatically create:
   - Redis instance
   - `REDIS_URL` environment variable

**Format**: `redis://default:PASSWORD@HOST:PORT`

## 🌐 Step 5: Create API Service

### 5.1 Add Service from GitHub

1. Click **"+ New"**
2. Select **"GitHub Repo"** (or **"Empty Service"** if repo already connected)
3. Select your repository
4. Railway will auto-detect it's a Python project

### 5.2 Configure Service Settings

In the service settings:

**Root Directory**: `backend`

**Start Command**: (Leave empty - uses Procfile)

**Build Command**: (Leave empty - auto-detected)

**Healthcheck Path**: `/graphql/` or `/health/`

### 5.3 Environment Variables

Click on the **"Variables"** tab and add these environment variables:

#### Required Environment Variables

```env
# Django Settings
DJANGO_SETTINGS_MODULE=saleor.settings.base
SECRET_KEY=your-very-secure-secret-key-here-generate-a-long-random-string
DEBUG=False
ALLOWED_HOSTS=*.railway.app,your-custom-domain.com

# Database (Auto-created by Railway PostgreSQL service)
# DATABASE_URL is automatically added by Railway
# No need to manually add it

# Redis (Auto-created by Railway Redis service)
# REDIS_URL is automatically added by Railway
# No need to manually add it

# Celery
CELERY_BROKER_URL=${REDIS_URL}
CELERY_RESULT_BACKEND=${REDIS_URL}

# AWS S3 (for media files)
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_STORAGE_BUCKET_NAME=grand-gold-media
AWS_S3_REGION_NAME=us-east-1
AWS_S3_CUSTOM_DOMAIN=grand-gold-media.s3.amazonaws.com
AWS_DEFAULT_ACL=public-read

# Email Configuration (SendGrid recommended)
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

# Payment Gateways
STRIPE_PUBLIC_KEY=pk_live_your_stripe_public_key
STRIPE_SECRET_KEY=sk_live_your_stripe_secret_key
RAZORPAY_KEY_ID=your_razorpay_key_id
RAZORPAY_KEY_SECRET=your_razorpay_key_secret
PAYTABS_PROFILE_ID=your_paytabs_profile_id
PAYTABS_SERVER_KEY=your_paytabs_server_key

# Sentry (Error Tracking - Optional but recommended)
SENTRY_DSN=your-sentry-dsn-url
```

#### Generating SECRET_KEY

Generate a secure SECRET_KEY:

```bash
# In your local terminal
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

Or use this online generator: https://djecrety.ir/

### 5.4 Resource Allocation

In the **"Settings"** → **"Resources"** section:

- **Memory**: 1GB (start with this, increase if needed)
- **CPU**: 1 vCPU

## ⚙️ Step 6: Create Celery Worker Service

### 6.1 Add Worker Service

1. Click **"+ New"** → **"Empty Service"**
2. Connect to the same GitHub repository
3. Set **Root Directory**: `backend`
4. Set **Start Command**: `worker` (from Procfile)

### 6.2 Configure Environment Variables

1. Click **"Variables"** tab
2. Click **"Reference Variables"**
3. Select your API service to copy all environment variables
4. Or manually add the same variables as the API service

### 6.3 Resource Allocation

- **Memory**: 512MB
- **CPU**: 0.5 vCPU

## ⏰ Step 7: Create Celery Beat Service

### 7.1 Add Beat Service

1. Click **"+ New"** → **"Empty Service"**
2. Connect to the same GitHub repository
3. Set **Root Directory**: `backend`
4. Set **Start Command**: `beat` (from Procfile)

### 7.2 Configure Environment Variables

Same as Worker service - reference from API service.

### 7.3 Resource Allocation

- **Memory**: 256MB
- **CPU**: 0.5 vCPU

## 🔄 Step 8: Run Database Migrations

### 8.1 Option 1: Via Railway CLI (Recommended)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Link to your project
cd backend
railway link

# Run migrations
railway run python manage.py migrate
```

### 8.2 Option 2: Via Railway Shell

1. Go to your API service in Railway dashboard
2. Click on **"Deployments"** tab
3. Click on the latest deployment
4. Click **"View Logs"**
5. Or use the **"Shell"** option if available

### 8.3 Option 3: Add Migration Service (One-time)

Create a temporary service just for migrations:

1. **"+ New"** → **"Empty Service"**
2. Root Directory: `backend`
3. Start Command: `python manage.py migrate && sleep 3600`
4. Run it once, then delete the service

### 8.4 Create Superuser

After migrations, create a superuser:

```bash
railway run python manage.py createsuperuser
```

Or via Railway shell with interactive mode.

## 📝 Step 9: Verify Procfile

Ensure your `backend/Procfile` exists and contains:

```
web: gunicorn saleor.wsgi:application --bind 0.0.0.0:$PORT --workers 4 --timeout 120
worker: celery -A saleor worker -l info --concurrency=4
beat: celery -A saleor beat -l info
```

## 🏗️ Step 10: Configure Settings for Railway

### 10.1 Update base.py for Production

Add to `backend/saleor/settings/base.py`:

```python
import os

# Railway-specific settings
if os.environ.get('RAILWAY_ENVIRONMENT'):
    # Use Railway's PORT
    ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*.railway.app').split(',')
    
    # Database (Railway provides DATABASE_URL)
    import dj_database_url
    if 'DATABASE_URL' in os.environ:
        DATABASES = {
            'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))
        }
    
    # Static files (use WhiteNoise)
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    
    # Media files (use S3)
    if 'AWS_STORAGE_BUCKET_NAME' in os.environ:
        DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
        STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'
```

### 10.2 Add dj-database-url to requirements.txt

Ensure `requirements.txt` includes:

```
dj-database-url>=2.1.0
```

## 🔐 Step 11: Set Up AWS S3 (Optional but Recommended)

### 11.1 Create S3 Bucket

1. Go to AWS Console → S3
2. Click **"Create bucket"**
3. Name: `grand-gold-media`
4. Region: Choose closest to your Railway region
5. Uncheck **"Block all public access"** (or configure CORS properly)
6. Click **"Create bucket"**

### 11.2 Configure CORS

In your S3 bucket → **"Permissions"** → **"CORS"**:

```json
[
    {
        "AllowedHeaders": ["*"],
        "AllowedMethods": ["GET", "PUT", "POST", "DELETE"],
        "AllowedOrigins": ["https://*.railway.app", "https://yourdomain.com"],
        "ExposeHeaders": ["ETag"]
    }
]
```

### 11.3 Create IAM User

1. Go to AWS IAM → Users
2. Click **"Create user"**
3. Username: `railway-grandgold`
4. Access type: **Programmatic access**
5. Attach policy: **AmazonS3FullAccess** (or create custom policy)
6. Save **Access Key ID** and **Secret Access Key**

Add these to Railway environment variables.

## 🌍 Step 12: Configure Custom Domain (Optional)

### 12.1 Add Domain in Railway

1. Go to your API service → **"Settings"** → **"Domains"**
2. Click **"Generate Domain"** for Railway domain (auto-generated)
3. Or click **"Custom Domain"** for your own domain
4. Enter your domain: `api.grandgold.com`

### 12.2 Configure DNS

Railway will provide DNS instructions:

1. Add a **CNAME** record:
   - Name: `api` (or `@` for root)
   - Value: Railway-provided domain
   - TTL: 300

2. Or add an **A** record if using root domain:
   - Railway will provide the IP address

### 12.3 Update ALLOWED_HOSTS

Update `ALLOWED_HOSTS` in Railway environment variables:

```
ALLOWED_HOSTS=*.railway.app,api.grandgold.com,www.grandgold.com
```

## ✅ Step 13: Verify Deployment

### 13.1 Check Service Status

All services should show **"Active"** status:
- ✅ PostgreSQL (Database)
- ✅ Redis (Cache/Queue)
- ✅ API Service (Web)
- ✅ Celery Worker
- ✅ Celery Beat

### 13.2 Test GraphQL Endpoint

1. Get your Railway domain from API service
2. Visit: `https://your-service.railway.app/graphql/`
3. You should see the GraphQL playground/interface

### 13.3 Test Health Check

Visit: `https://your-service.railway.app/health/` (if configured)

Or test GraphQL query:

```graphql
{
  __schema {
    types {
      name
    }
  }
}
```

### 13.4 Check Logs

1. Go to each service → **"Deployments"** → **"View Logs"**
2. Look for errors or warnings
3. Verify all services are running correctly

## 🔧 Step 14: Monitor & Troubleshoot

### 14.1 Monitor Resource Usage

- Go to each service → **"Metrics"**
- Monitor CPU, Memory, Network usage
- Scale up if needed

### 14.2 View Logs

- Real-time logs: Service → **"Deployments"** → **"View Logs"**
- Historical logs: Service → **"Logs"** tab

### 14.3 Common Issues

#### Database Connection Errors

- Verify `DATABASE_URL` is set correctly
- Check database service is running
- Verify migrations ran successfully

#### Redis Connection Errors

- Verify `REDIS_URL` is set correctly
- Check Redis service is running
- Ensure Celery services reference the same Redis URL

#### Static Files Not Loading

- Ensure WhiteNoise is in requirements.txt
- Verify `STATIC_ROOT` is configured
- Run `python manage.py collectstatic` during deployment

#### Memory Issues

- Increase memory allocation in service settings
- Check for memory leaks in logs
- Optimize database queries

## 📊 Step 15: Initial Data Setup

### 15.1 Run Initial Data Script

```bash
railway run python manage.py shell
```

Then in the shell:

```python
exec(open('create_initial_data.py').read())
```

Or create a management command and run:

```bash
railway run python manage.py load_initial_data
```

### 15.2 Verify Data

- Check Django admin: `https://your-service.railway.app/admin/`
- Verify regions, currencies, branches are created
- Test GraphQL queries

## 🎯 Step 16: Final Checklist

- [ ] All services deployed and running
- [ ] Database migrations completed
- [ ] Environment variables configured
- [ ] Custom domain configured (if applicable)
- [ ] AWS S3 configured (if using)
- [ ] GraphQL endpoint accessible
- [ ] Admin panel accessible
- [ ] Celery worker processing tasks
- [ ] Celery beat scheduling tasks
- [ ] Initial data loaded
- [ ] Logs show no critical errors
- [ ] Health checks passing

## 🔄 Continuous Deployment

Railway automatically deploys when you push to your connected branch:

1. Push code to GitHub: `git push origin main`
2. Railway detects the push
3. Automatically builds and deploys
4. Your changes go live!

## 💰 Cost Estimation

**Railway Pricing** (as of 2024):

- **PostgreSQL**: ~$5-20/month (depending on size)
- **Redis**: ~$5-10/month
- **API Service**: Pay-as-you-go (~$5-20/month for moderate traffic)
- **Worker Service**: ~$5-10/month
- **Beat Service**: ~$2-5/month

**Total Estimated**: ~$25-65/month for a small-to-medium deployment

**AWS S3**: ~$0.023/GB storage + $0.005/1000 requests

## 📚 Additional Resources

- [Railway Documentation](https://docs.railway.app)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [Saleor Deployment Guide](https://docs.saleor.io/docs/3.x/developer/deployment)

## 🆘 Support

If you encounter issues:

1. Check Railway logs
2. Verify environment variables
3. Test locally first
4. Check Railway status page
5. Review Django/Saleor documentation

---

**Congratulations!** Your multi-branch jewellery platform is now deployed on Railway! 🎉


