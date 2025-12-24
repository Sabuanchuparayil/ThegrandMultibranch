"""
Saleor Settings Template

Copy relevant sections to your saleor/settings/base.py or saleor/settings/local.py

After Saleor is installed, add your apps to INSTALLED_APPS and configure middleware.
"""

# ============================================================================
# INSTALLED_APPS
# ============================================================================
# Add these to your existing INSTALLED_APPS list in saleor/settings/base.py

INSTALLED_APPS_EXTENSIONS = [
    # Regions and Currency
    'saleor_extensions.regions',
    'saleor_extensions.currency',
    
    # Branches and Inventory
    'saleor_extensions.branches',
    'saleor_extensions.inventory',
    
    # Pricing and Taxes
    'saleor_extensions.pricing',
    'saleor_extensions.taxes',
    
    # Orders and Products
    'saleor_extensions.orders',
    'saleor_extensions.products',
    
    # Fulfillment and Returns
    'saleor_extensions.fulfillment',
    'saleor_extensions.returns',
    
    # Customers and Marketing
    'saleor_extensions.customers',
    'saleor_extensions.promotions',
    
    # Content and Communication
    'saleor_extensions.cms',
    'saleor_extensions.notifications',
    
    # Financial and Integration
    'saleor_extensions.payments',
    'saleor_extensions.invoices',
    'saleor_extensions.reports',
    'saleor_extensions.integrations',
    
    # System
    'saleor_extensions.audit',
    'saleor_extensions.permissions',
]

# Example of how to add to your settings file:
# INSTALLED_APPS = [
#     # ... existing Saleor apps ...
#     *INSTALLED_APPS_EXTENSIONS,
# ]

# ============================================================================
# MIDDLEWARE
# ============================================================================
# Add audit logging middleware to your MIDDLEWARE list

MIDDLEWARE_EXTENSIONS = [
    # Add this after authentication middleware, before view middleware
    'saleor_extensions.audit.middleware.AuditLogMiddleware',
]

# Example:
# MIDDLEWARE = [
#     'django.middleware.security.SecurityMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     # ... other middleware ...
#     'saleor_extensions.audit.middleware.AuditLogMiddleware',  # Add here
#     'django.middleware.common.CommonMiddleware',
#     # ... rest of middleware ...
# ]

# ============================================================================
# DATABASE CONFIGURATION
# ============================================================================
# Your existing database configuration should work fine.
# Ensure PostgreSQL is configured for Saleor.

# ============================================================================
# CELERY CONFIGURATION
# ============================================================================
# Add custom Celery tasks if needed

# from celery.schedules import crontab
# 
# CELERY_BEAT_SCHEDULE = {
#     # ... existing Saleor tasks ...
#     
#     # Currency rate updates
#     'update-currency-rates': {
#         'task': 'saleor_extensions.tasks.update_currency_rates',
#         'schedule': crontab(hour=0, minute=0),  # Daily at midnight
#     },
#     
#     # Gold rate updates
#     'update-gold-rates': {
#         'task': 'saleor_extensions.tasks.update_gold_rates',
#         'schedule': crontab(minute=0),  # Hourly
#     },
#     
#     # Scheduled reports
#     'generate-scheduled-reports': {
#         'task': 'saleor_extensions.tasks.generate_scheduled_reports',
#         'schedule': crontab(hour=6, minute=0),  # Daily at 6 AM
#     },
# }

# ============================================================================
# GRAPHQL CONFIGURATION
# ============================================================================
# Custom GraphQL schema extensions will be registered in saleor's schema.py

# ============================================================================
# AWS S3 CONFIGURATION (for media files)
# ============================================================================
# Add to your settings if using S3 for media storage

# AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
# AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
# AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', 'us-east-1')
# AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
# AWS_DEFAULT_ACL = 'public-read'
# 
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'

# ============================================================================
# CURRENCY AND GOLD RATE API KEYS
# ============================================================================
# Add these to your environment variables

# CURRENCY_API_KEY = os.environ.get('CURRENCY_API_KEY')
# GOLD_RATE_API_KEY_UK = os.environ.get('GOLD_RATE_API_KEY_UK')
# GOLD_RATE_API_KEY_UAE = os.environ.get('GOLD_RATE_API_KEY_UAE')
# GOLD_RATE_API_KEY_INDIA = os.environ.get('GOLD_RATE_API_KEY_INDIA')

# ============================================================================
# PAYMENT GATEWAY CONFIGURATION
# ============================================================================
# Payment gateway keys should be set in PaymentGateway model via admin
# But you can also set defaults here if needed

# STRIPE_PUBLIC_KEY = os.environ.get('STRIPE_PUBLIC_KEY')
# STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
# RAZORPAY_KEY_ID = os.environ.get('RAZORPAY_KEY_ID')
# RAZORPAY_KEY_SECRET = os.environ.get('RAZORPAY_KEY_SECRET')

# ============================================================================
# NOTIFICATION SETTINGS
# ============================================================================
# Email, SMS, WhatsApp configuration

# EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.sendgrid.net')
# EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
# EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================
# Add custom logging if needed

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'file': {
#             'level': 'INFO',
#             'class': 'logging.FileHandler',
#             'filename': 'logs/extensions.log',
#         },
#     },
#     'loggers': {
#         'saleor_extensions': {
#             'handlers': ['file'],
#             'level': 'INFO',
#             'propagate': True,
#         },
#     },
# }

