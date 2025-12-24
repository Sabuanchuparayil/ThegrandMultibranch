"""
Django settings for Grand Gold & Diamonds project.

This module extends Saleor's default settings with our custom configurations.
We import from the installed Saleor package and then apply our extensions.
"""

# First, try to import Saleor settings
# When Saleor is installed from GitHub, it provides saleor.settings module
import sys

# Store original modules to avoid conflicts
_original_modules = {}
if 'saleor' in sys.modules:
    _original_modules['saleor'] = sys.modules['saleor']
if 'saleor.settings' in sys.modules:
    _original_modules['saleor.settings'] = sys.modules['saleor.settings']

# Try to import from installed Saleor package
try:
    # Remove our local saleor from modules temporarily if it exists
    if 'saleor' in sys.modules and 'saleor' not in _original_modules:
        del sys.modules['saleor']
    if 'saleor.settings' in sys.modules and 'saleor.settings' not in _original_modules:
        del sys.modules['saleor.settings']
    
    # Import installed Saleor settings
    import importlib
    saleor_settings_module = importlib.import_module('saleor.settings')
    
    # Copy all public attributes to our namespace
    for attr_name in dir(saleor_settings_module):
        if not attr_name.startswith('_'):
            try:
                attr_value = getattr(saleor_settings_module, attr_name)
                # Only copy module-level attributes (not methods, classes, etc.)
                if not callable(attr_value) or attr_name.isupper():
                    globals()[attr_name] = attr_value
            except (AttributeError, TypeError):
                pass
                
except ImportError as e:
    # Restore original modules
    for key, value in _original_modules.items():
        sys.modules[key] = value
    
    raise ImportError(
        f"Could not import Saleor settings from installed package: {e}. "
        "Make sure Saleor is installed: pip install git+https://github.com/saleor/saleor.git"
    )

# Verify INSTALLED_APPS was imported
if 'INSTALLED_APPS' not in globals():
    raise ImportError(
        "INSTALLED_APPS not found after importing Saleor settings. "
        "The Saleor package may have a different settings structure."
    )

# Now extend INSTALLED_APPS with our custom extensions
INSTALLED_APPS = list(INSTALLED_APPS) + [  # noqa: F405
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

# Ensure MIDDLEWARE exists
if 'MIDDLEWARE' not in globals():
    MIDDLEWARE = []

# Add audit middleware after AuthenticationMiddleware
if 'saleor_extensions.audit.middleware.AuditLogMiddleware' not in MIDDLEWARE:  # noqa: F405
    try:
        auth_index = MIDDLEWARE.index('django.contrib.auth.middleware.AuthenticationMiddleware')  # noqa: F405
        MIDDLEWARE.insert(auth_index + 1, 'saleor_extensions.audit.middleware.AuditLogMiddleware')  # noqa: F405
    except ValueError:
        MIDDLEWARE.append('saleor_extensions.audit.middleware.AuditLogMiddleware')  # noqa: F405

# Railway-specific configurations
import os

# Database configuration (Railway provides DATABASE_URL)
if 'DATABASE_URL' in os.environ:
    try:
        import dj_database_url
        DATABASES = {
            'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))
        }
    except ImportError:
        pass

# Static files configuration for Railway
STATIC_ROOT = os.path.join(os.path.dirname(__file__), 'staticfiles')

# Media files - use S3 if configured
if 'AWS_STORAGE_BUCKET_NAME' in os.environ:
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', 'us-east-1')
    AWS_S3_CUSTOM_DOMAIN = os.environ.get('AWS_S3_CUSTOM_DOMAIN', f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com')
    AWS_DEFAULT_ACL = 'public-read'
