# Railway Quick Reference Card

## 🚀 Essential Railway Commands & Info

### Railway CLI Installation

```bash
npm i -g @railway/cli
railway login
```

### Common Railway CLI Commands

```bash
# Link to project
railway link

# View services
railway status

# Set environment variable
railway variables set KEY=value

# View logs
railway logs

# Run command in service
railway run python manage.py migrate

# Open service in browser
railway open
```

## 📋 Railway Service Checklist

### Services to Create

- [ ] **PostgreSQL** - Database
  - Auto-creates `DATABASE_URL`
  
- [ ] **Redis** - Cache & Queue
  - Auto-creates `REDIS_URL`
  
- [ ] **backend-api** - Django/Saleor API
  - Root: `backend`
  - Start: (from Procfile)
  
- [ ] **celery-worker** - Background tasks
  - Root: `backend`
  - Start: `celery -A saleor worker -l info`
  
- [ ] **celery-beat** - Scheduled tasks
  - Root: `backend`
  - Start: `celery -A saleor beat -l info`

## 🔑 Critical Environment Variables

```bash
SECRET_KEY=<generate-with-python>
DEBUG=False
ALLOWED_HOSTS=*.railway.app,your-domain.com

# AWS S3 (Required)
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_STORAGE_BUCKET_NAME=grand-gold-media
AWS_S3_REGION_NAME=us-east-1

# Payment Gateways
STRIPE_SECRET_KEY=...
RAZORPAY_KEY_SECRET=...
PAYTABS_SERVER_KEY=...

# Email
EMAIL_HOST=smtp.sendgrid.net
EMAIL_HOST_PASSWORD=...
```

## 🔍 Verification URLs

After deployment:

- **GraphQL API**: `https://your-app.railway.app/graphql/`
- **Admin Panel**: `https://your-app.railway.app/dashboard/`
- **Health Check**: `https://your-app.railway.app/health/`

## 📊 Resource Limits (Free Tier)

- **512 MB RAM** per service
- **$5 credit** per month
- **100 GB** bandwidth

## 🆘 Quick Troubleshooting

**Build Fails?**
→ Check `requirements.txt` and `runtime.txt`

**Database Connection Error?**
→ Verify `DATABASE_URL` is set (auto-created)

**Static Files 404?**
→ Run `collectstatic` in build command

**Environment Variables Not Working?**
→ Restart service after adding variables

---

For complete setup guide, see: `RAILWAY_AND_GITHUB_SETUP.md`

