# Saleor Integration Guide

## Overview

This guide will help you integrate the custom extensions with Saleor core.

## Prerequisites

1. Saleor 3.20+ installed
2. PostgreSQL database configured
3. Redis configured
4. Python 3.11+ environment

## Step 1: Install Saleor

```bash
cd backend
source venv/bin/activate  # or activate your virtual environment
pip install saleor>=3.20.0
```

## Step 2: Initialize Saleor Project

If you haven't already initialized Saleor, follow their installation guide:
https://docs.saleor.io/docs/3.x/developer/installation

Your project structure should look like:
```
backend/
├── saleor/              # Saleor core (you'll get this from Saleor installation)
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── local.py
│   │   └── production.py
│   ├── urls.py
│   └── wsgi.py
├── saleor_extensions/   # Your custom apps (already created)
└── manage.py
```

## Step 3: Update Settings

Update `saleor/settings/base.py` or create `saleor/settings/local.py`:

```python
# Add your apps to INSTALLED_APPS
INSTALLED_APPS = [
    # ... existing Saleor apps ...
    
    # Your custom extensions
    'saleor_extensions.regions',
    'saleor_extensions.currency',
    'saleor_extensions.branches',
    'saleor_extensions.inventory',
    'saleor_extensions.pricing',
    'saleor_extensions.taxes',
    'saleor_extensions.orders',
    'saleor_extensions.products',
    'saleor_extensions.fulfillment',
    'saleor_extensions.returns',
    'saleor_extensions.customers',
    'saleor_extensions.promotions',
    'saleor_extensions.cms',
    'saleor_extensions.notifications',
    'saleor_extensions.payments',
    'saleor_extensions.invoices',
    'saleor_extensions.reports',
    'saleor_extensions.integrations',
    'saleor_extensions.audit',
    'saleor_extensions.permissions',
]

# Add middleware
MIDDLEWARE = [
    # ... existing middleware ...
    'saleor_extensions.audit.middleware.AuditLogMiddleware',
]
```

## Step 4: Update Models with ForeignKeys

See `MODEL_UPDATES.md` for detailed instructions on updating each model.

Key models to update:
1. `orders/models.py` - Link to `saleor.order.models.Order`
2. `products/models.py` - Link to `saleor.product.models.Product`
3. `customers/models.py` - Link to `saleor.account.models.User`
4. `inventory/models.py` - Link to products
5. `invoices/models.py` - Link to orders
6. `payments/models.py` - Link to orders

## Step 5: Create Migrations

```bash
# First, run Saleor's migrations
python manage.py migrate

# Then create migrations for your extensions
python manage.py makemigrations regions
python manage.py makemigrations currency
python manage.py makemigrations branches
# ... repeat for all 20 apps ...

# Or create all at once
python manage.py makemigrations

# Apply all migrations
python manage.py migrate
```

## Step 6: Create Initial Data

```bash
# Create superuser
python manage.py createsuperuser

# Load initial data (if you create fixtures)
python manage.py loaddata initial_data.json
```

## Step 7: Test Integration

1. Start server: `python manage.py runserver`
2. Visit admin: `http://localhost:8000/admin`
3. Test creating records with ForeignKey relationships
4. Verify data integrity

## Troubleshooting

### Import Errors
If you get `ImportError: No module named 'saleor'`:
- Make sure Saleor is installed: `pip list | grep saleor`
- Check Python path and virtual environment

### Migration Conflicts
- Always run Saleor migrations first
- If conflicts occur, review migration files carefully
- Consider starting fresh with a new database if in early development

### ForeignKey Errors
- Ensure Saleor models exist (run Saleor migrations first)
- Check app names are correct (e.g., 'order.Order', not 'saleor.order.Order')
- Verify INSTALLED_APPS includes both Saleor apps and your extensions

## Next Steps

After successful integration:
1. Build GraphQL APIs (see `NEXT_STEPS_ROADMAP.md`)
2. Complete service implementations
3. Set up Celery tasks
4. Build frontend interfaces


