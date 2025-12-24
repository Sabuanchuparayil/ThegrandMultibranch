"""
Django settings for Grand Gold & Diamonds project.

This module extends Saleor's default settings with our custom configurations.
We import from the installed Saleor package and then apply our extensions.
"""

import sys
import os

# Critical: Ensure we import from installed package, not our local saleor directory
# Remove local saleor from sys.modules and sys.path to force import from site-packages
_backend_dir = os.path.dirname(os.path.abspath(__file__))
_local_saleor_path = os.path.join(_backend_dir, 'saleor')

# Remove local saleor directory from sys.path if it's there
if _backend_dir in sys.path:
    sys.path.remove(_backend_dir)

# Temporarily remove any saleor modules from sys.modules
_local_modules = {}
for key in list(sys.modules.keys()):
    if key.startswith('saleor'):
        _local_modules[key] = sys.modules.pop(key)

try:
    # Now import from installed Saleor package
    import importlib
    
    # Import the installed Saleor settings module
    # This will now find it in site-packages, not our local directory
    saleor_settings_module = importlib.import_module('saleor.settings')
    
    # Copy all uppercase attributes (Django settings are uppercase)
    # Also copy some important non-uppercase attributes that Saleor might use
    for attr_name in dir(saleor_settings_module):
        if attr_name.startswith('_'):
            continue
        
        try:
            attr_value = getattr(saleor_settings_module, attr_name)
            
            # Copy all uppercase attributes (these are Django settings)
            if attr_name.isupper():
                globals()[attr_name] = attr_value
            # Also handle special cases if needed
            elif attr_name in ('default_settings', 'settings', 'SETTINGS'):
                # Some Saleor versions might use these
                globals()[attr_name] = attr_value
        except (AttributeError, TypeError):
            continue
    
    # Explicitly check for and copy INSTALLED_APPS if it exists
    if hasattr(saleor_settings_module, 'INSTALLED_APPS'):
        INSTALLED_APPS = getattr(saleor_settings_module, 'INSTALLED_APPS')
        globals()['INSTALLED_APPS'] = INSTALLED_APPS
    
    # Explicitly check for and copy MIDDLEWARE if it exists
    if hasattr(saleor_settings_module, 'MIDDLEWARE'):
        MIDDLEWARE = getattr(saleor_settings_module, 'MIDDLEWARE')
        globals()['MIDDLEWARE'] = MIDDLEWARE
        
except ImportError as e:
    # Restore local modules if import failed
    for key, value in _local_modules.items():
        sys.modules[key] = value
    # Restore backend dir to path
    if _backend_dir not in sys.path:
        sys.path.insert(0, _backend_dir)
    
    raise ImportError(
        f"Could not import Saleor settings from installed package: {e}. "
        "Make sure Saleor is installed: pip install git+https://github.com/saleor/saleor.git"
    )
finally:
    # Always restore backend dir to path (we need it for our extensions)
    if _backend_dir not in sys.path:
        sys.path.insert(0, _backend_dir)

# Verify INSTALLED_APPS was imported
if 'INSTALLED_APPS' not in globals():
    # Last resort: try to inspect the module more carefully
    try:
        import saleor.settings as ss
        if hasattr(ss, 'INSTALLED_APPS'):
            INSTALLED_APPS = ss.INSTALLED_APPS
            globals()['INSTALLED_APPS'] = INSTALLED_APPS
        else:
            # List what attributes ARE available for debugging
            available = [a for a in dir(ss) if a.isupper()]
            raise ImportError(
                f"INSTALLED_APPS not found in Saleor settings. "
                f"Available uppercase attributes: {available[:10]}. "
                "The Saleor package may have a different settings structure."
            )
    except Exception as e2:
        raise ImportError(
            f"INSTALLED_APPS not found after importing Saleor settings. "
            f"Import error: {e2}. "
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
