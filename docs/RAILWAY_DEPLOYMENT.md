# Railway Deployment Guide

This guide walks you through deploying the Grand Gold multi-region e-commerce backend to Railway.

## Prerequisites

1. Railway account (sign up at https://railway.app)
2. GitHub account with repository access
3. AWS account (for S3 media storage)

## Step 1: Create Railway Account & Project

1. Go to https://railway.app
2. Sign up/Login with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo" (or create empty project)

## Step 2: Connect Repository

If not already done, initialize Git and push to GitHub:

```bash
cd "/Users/apple/Desktop/Grand Gold/The grand-Multibranch"
git init
git add .
git commit -m "Initial commit: Multi-region jewellery platform"

# Create GitHub repository and push
git remote add origin <your-github-repo-url>
git push -u origin main
```

Then connect to Railway via GitHub integration in the Railway dashboard.

## Step 3: Set Up Railway Services

### 3.1: Add PostgreSQL Database

1. In Railway dashboard, click "+ New"
2. Select "Database" → "Add PostgreSQL"
3. Railway will automatically create `DATABASE_URL` environment variable
4. Note the connection string

### 3.2: Add Redis Service

1. Click "+ New"
2. Select "Database" → "Add Redis"
3. Railway will create `REDIS_URL` environment variable

### 3.3: Create API Service

1. Click "+ New" → "GitHub Repo"
2. Select your repository
3. Railway will auto-detect Python and use `Procfile`
4. Set root directory to `/backend` if backend is in subfolder
5. Start command: Leave empty (uses Procfile `web` command)

**Settings:**
- **Root Directory**: `backend` (if backend is in subfolder)
- **Start Command**: (leave empty, uses Procfile)
- **Healthcheck Path**: `/graphql/`
- **Port**: Railway will set $PORT automatically

### 3.4: Create Celery Worker Service

1. In same project, click "+ New" → "Empty Service"
2. Connect to same GitHub repo
3. Set root directory to `/backend`
4. Set start command: `worker` (references Procfile)
5. Copy environment variables from API service (use "Shared" variables)

### 3.5: Create Celery Beat Service

1. Click "+ New" → "Empty Service"
2. Connect to same GitHub repo
3. Set root directory to `/backend`
4. Set start command: `beat` (references Procfile)
5. Copy environment variables from API service

## Step 4: Configure Environment Variables

In Railway, go to each service → "Variables" tab and add:

### Database & Redis (Auto-created by Railway)
- `DATABASE_URL` - Automatically created when PostgreSQL service is added
- `REDIS_URL` - Automatically created when Redis service is added

### Django Settings
```
SECRET_KEY=<generate-strong-secret-key>
DEBUG=False
ALLOWED_HOSTS=your-domain.railway.app,your-custom-domain.com
```

To generate a secret key:
```python
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

### AWS S3 (Required for media files)
```
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=grand-gold-media
AWS_S3_REGION_NAME=us-east-1
```

**To set up AWS S3:**
1. Go to AWS Console → S3
2. Create bucket: `grand-gold-media`
3. Configure CORS for web access
4. Create IAM user with S3 permissions
5. Generate access keys

### Currency & Gold Rate APIs
```
CURRENCY_API_KEY=your-key
GOLD_RATE_API_KEY_UK=your-key
GOLD_RATE_API_KEY_UAE=your-key
GOLD_RATE_API_KEY_INDIA=your-key
```

### Payment Gateways

**UK:**
```
STRIPE_PUBLIC_KEY=your-key
STRIPE_SECRET_KEY=your-key
```

**UAE:**
```
PAYTABS_PROFILE_ID=your-key
PAYTABS_SERVER_KEY=your-key
```

**India:**
```
RAZORPAY_KEY_ID=your-key
RAZORPAY_KEY_SECRET=your-key
```

### Email
```
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=your-sendgrid-key
```

### Sentry (Optional but recommended)
```
SENTRY_DSN=your-sentry-dsn
```

### Mark Variables as Shared

For variables needed by multiple services (DATABASE_URL, REDIS_URL, SECRET_KEY, etc.):
1. Click on the variable
2. Enable "Shared" toggle
3. All services in the project will have access

## Step 5: Resource Allocation

Configure resource limits for each service:

- **API Service**: 1GB RAM, 1 vCPU (start with this, scale as needed)
- **Worker Service**: 512MB RAM, 0.5 vCPU
- **Beat Service**: 256MB RAM, 0.5 vCPU

To configure:
1. Click on service
2. Go to "Settings" → "Resources"
3. Adjust CPU and Memory limits

## Step 6: Run Database Migrations

### Option 1: Via Railway CLI

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Link to project
railway link

# Run migrations
railway run python manage.py migrate
```

### Option 2: Via Railway Shell

1. In Railway dashboard, click on API service
2. Click "Deployments" → Click on latest deployment
3. Open "Shell" tab
4. Run: `python manage.py migrate`

## Step 7: Configure Custom Domain (Optional)

1. In Railway, click on API service
2. Go to "Settings" → "Domains"
3. Click "Generate Domain" for Railway domain (e.g., `your-app.railway.app`)
4. Or add custom domain:
   - Click "Custom Domain"
   - Enter your domain (e.g., `api.grandgold.com`)
   - Configure DNS as instructed by Railway
   - Railway will provision SSL certificate automatically

## Step 8: Verify Deployment

1. Check all services are running in Railway dashboard
2. Verify API endpoint: `https://your-domain.railway.app/graphql/`
3. Test GraphQL queries
4. Check logs for errors
5. Verify database migrations ran successfully

## Troubleshooting

### Service Won't Start
- Check logs in Railway dashboard
- Verify environment variables are set correctly
- Ensure `Procfile` is in the root directory (or adjust root directory in service settings)

### Database Connection Errors
- Verify `DATABASE_URL` is set correctly
- Check PostgreSQL service is running
- Ensure database exists (Railway creates it automatically)

### Redis Connection Errors
- Verify `REDIS_URL` is set correctly
- Check Redis service is running

### Migration Errors
- Run migrations manually via Railway CLI or shell
- Check database logs for specific errors
- Ensure all required Django apps are installed in settings

## Monitoring

- View logs: Click on service → "Deployments" → Click deployment → View logs
- Set up alerts: Railway automatically monitors service health
- Add Sentry for error tracking (recommended)

## Scaling

To scale services:
1. Click on service
2. Go to "Settings" → "Resources"
3. Increase CPU/Memory as needed
4. Railway will automatically restart the service with new resources


