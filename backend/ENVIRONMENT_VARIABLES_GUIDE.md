# Environment Variables Guide for Railway Deployment

This guide explains how to generate and configure all required environment variables for your Grand Gold & Diamonds application on Railway.

## Quick Start

1. **Generate secrets** using the provided script:
   ```bash
   cd backend
   python3 generate_secrets.py
   ```

2. **Copy the generated values** to Railway environment variables

3. **Set them in Railway** dashboard under your service → Variables

## Required Environment Variables

### 1. SECRET_KEY (Required)

**Purpose**: Django's secret key for cryptographic signing

**Generate**:
```bash
# Using Django (if installed)
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Or using Python secrets module
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

**Or use the script**:
```bash
python3 generate_secrets.py
```

**Set in Railway**: `SECRET_KEY=your-generated-key-here`

---

### 2. RSA_PRIVATE_KEY (Required for Saleor JWT)

**Purpose**: RSA private key for Saleor's JWT token authentication

**Generate**:
```bash
# Using the provided script (recommended)
python3 generate_secrets.py

# Or manually using OpenSSL
openssl genrsa -out private_key.pem 2048
cat private_key.pem
```

**Important**: The key must be in PEM format and include the full key with headers:
```
-----BEGIN PRIVATE KEY-----
...
-----END PRIVATE KEY-----
```

**Set in Railway**: `RSA_PRIVATE_KEY=-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----`

**Note**: When setting in Railway, you may need to escape newlines as `\n` or paste the entire key including newlines.

---

### 3. ALLOWED_HOSTS (Recommended)

**Purpose**: List of allowed hostnames for your Django application

**Format**: Comma-separated list

**Set in Railway**: 
```
ALLOWED_HOSTS=your-app.railway.app,localhost,127.0.0.1
```

**To find your Railway domain**: Check your Railway service → Settings → Domains

---

### 4. DATABASE_URL (Usually Auto-provided)

**Purpose**: PostgreSQL connection string

**Format**: `postgresql://user:password@host:port/dbname`

**Railway**: Usually automatically provided when you add a PostgreSQL service

**If not auto-provided**, set manually:
```
DATABASE_URL=postgresql://postgres:password@containers-us-west-xxx.railway.app:5432/railway
```

---

### 5. REDIS_URL (Optional, if using Redis)

**Purpose**: Redis connection string for Celery and caching

**Format**: `redis://host:port` or `redis://:password@host:port`

**Railway**: Usually automatically provided when you add a Redis service

---

### 6. DEBUG (Recommended for Production)

**Purpose**: Enable/disable Django debug mode

**Set in Railway**: 
```
DEBUG=False
```

**Warning**: Never set `DEBUG=True` in production!

---

## Optional Environment Variables

### AWS S3 Storage (if using S3 for media files)

```
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_REGION_NAME=us-east-1
AWS_S3_CUSTOM_DOMAIN=your-bucket.s3.amazonaws.com
```

### Email Configuration (if using email)

```
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_USE_TLS=True
```

### Celery Configuration (if using Celery workers)

```
CELERY_BROKER_URL=redis://host:port
CELERY_RESULT_BACKEND=redis://host:port
```

---

## How to Set Environment Variables in Railway

### Method 1: Railway Dashboard (Recommended)

1. Go to your Railway project
2. Select your service
3. Click on **Variables** tab
4. Click **+ New Variable**
5. Enter variable name and value
6. Click **Add**

### Method 2: Railway CLI

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Link to your project
railway link

# Set variables
railway variables set SECRET_KEY="your-secret-key"
railway variables set RSA_PRIVATE_KEY="your-rsa-key"
```

### Method 3: railway.json (for static values only)

**Note**: Don't put secrets in railway.json as it's committed to git!

---

## Security Best Practices

1. **Never commit secrets to git**
   - Use `.env` files locally (add to `.gitignore`)
   - Use Railway environment variables for production

2. **Rotate keys regularly**
   - Change `SECRET_KEY` periodically
   - Regenerate `RSA_PRIVATE_KEY` if compromised

3. **Use different keys for different environments**
   - Development: Local `.env` file
   - Staging: Railway staging service variables
   - Production: Railway production service variables

4. **Restrict access**
   - Only team members who need access should see secrets
   - Use Railway's team permissions

---

## Verification

After setting environment variables:

1. **Redeploy your service** in Railway (variables are loaded at startup)

2. **Check logs** - warnings about missing keys should disappear:
   ```
   ✅ No more: "SECRET_KEY not configured"
   ✅ No more: "RSA_PRIVATE_KEY is missing"
   ```

3. **Test the application**:
   - Access your Railway domain
   - Try logging in (if authentication is set up)
   - Check that JWT tokens work (if using Saleor GraphQL)

---

## Troubleshooting

### Keys not working?

1. **Check format**: RSA keys must include `-----BEGIN PRIVATE KEY-----` headers
2. **Check newlines**: Some systems require `\n` instead of actual newlines
3. **Redeploy**: Environment variables are loaded at startup, so redeploy after changes

### Still seeing warnings?

1. **Verify variable names**: Must match exactly (case-sensitive)
2. **Check service**: Make sure you set variables on the correct service
3. **Redeploy**: Changes require a redeploy to take effect

---

## Quick Reference

| Variable | Required | Format | Example |
|----------|----------|--------|---------|
| `SECRET_KEY` | ✅ Yes | String | `django-insecure-...` |
| `RSA_PRIVATE_KEY` | ✅ Yes | PEM | `-----BEGIN PRIVATE KEY-----...` |
| `ALLOWED_HOSTS` | ⚠️ Recommended | Comma-separated | `app.railway.app,localhost` |
| `DATABASE_URL` | ✅ Yes | PostgreSQL URL | `postgresql://...` |
| `REDIS_URL` | ⚠️ Optional | Redis URL | `redis://...` |
| `DEBUG` | ⚠️ Recommended | Boolean | `False` |

---

## Need Help?

- Check Railway documentation: https://docs.railway.app
- Check Django documentation: https://docs.djangoproject.com
- Check Saleor documentation: https://docs.saleor.io

