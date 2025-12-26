"""
Saleor Settings Integration
Copy this to your saleor/settings/base.py or saleor/settings/local.py

This file shows exactly how to integrate your extensions with Saleor.
"""

# ============================================================================
# ADD TO INSTALLED_APPS
# ============================================================================
# In your saleor/settings/base.py, add these to INSTALLED_APPS:

INSTALLED_APPS = [
    # ... existing Saleor apps ...
    
    # Your custom extensions (add these 20 apps)
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
    
    # ... rest of Saleor apps ...
]

# ============================================================================
# ADD TO MIDDLEWARE
# ============================================================================
# In your saleor/settings/base.py, add to MIDDLEWARE (after auth middleware):

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    
    # Add audit logging middleware here
    'saleor_extensions.audit.middleware.AuditLogMiddleware',
    
    # ... rest of middleware ...
]

# ============================================================================
# CELERY BEAT SCHEDULE
# ============================================================================
# Add to your CELERY_BEAT_SCHEDULE if you want background tasks

from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    # ... existing Saleor tasks ...
    
    # Currency rate updates (daily at midnight)
    'update-currency-rates': {
        'task': 'saleor_extensions.tasks.update_currency_rates',
        'schedule': crontab(hour=0, minute=0),
    },
    
    # Gold rate updates (hourly)
    'update-gold-rates': {
        'task': 'saleor_extensions.tasks.update_gold_rates',
        'schedule': crontab(minute=0),
    },
    
    # Scheduled reports (daily at 6 AM)
    'generate-scheduled-reports': {
        'task': 'saleor_extensions.tasks.generate_scheduled_reports',
        'schedule': crontab(hour=6, minute=0),
    },
    
    # Send pending notifications (every 5 minutes)
    'send-pending-notifications': {
        'task': 'saleor_extensions.tasks.send_pending_notifications',
        'schedule': crontab(minute='*/5'),
    },
    
    # Low stock alerts (daily at 9 AM)
    'process-low-stock-alerts': {
        'task': 'saleor_extensions.tasks.process_low_stock_alerts',
        'schedule': crontab(hour=9, minute=0),
    },
}

# ============================================================================
# NOTES
# ============================================================================
# 1. After updating INSTALLED_APPS, run:
#    python manage.py makemigrations
#    python manage.py migrate
#
# 2. Make sure to update your models first (see MODEL_UPDATES.md)
#
# 3. Test in Django admin after integration
#
# 4. Check for any import errors or missing dependencies


