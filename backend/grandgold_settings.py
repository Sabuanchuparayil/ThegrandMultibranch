"""
Django settings for Grand Gold & Diamonds project.

This module extends Saleor's default settings with our custom configurations.
We import from the installed Saleor package and then apply our extensions.
"""

import sys
import os

# We need to import Saleor from the installed package, not our local saleor directory
# Instead of removing backend from sys.path (which breaks everything), we'll use a different strategy:
# Try importing directly and handle the conflict if it occurs

try:
    # First, try to import directly - if Saleor is installed correctly, this should work
    # even if our local saleor directory exists, Python should find the installed one first
    # (site-packages comes before current directory in Python's module search path)
    from saleor.settings import *  # noqa: F403, F405
    
except ImportError as e:
    # If that fails, try to import using importlib with explicit path handling
    try:
        import importlib.util
        import site
        
        # Find site-packages directory
        site_packages = None
        for path in site.getsitepackages():
            if 'site-packages' in path:
                saleor_path = os.path.join(path, 'saleor')
                if os.path.exists(saleor_path):
                    site_packages = path
                    break
        
        if site_packages:
            # Load saleor.settings from site-packages explicitly
            settings_file = os.path.join(site_packages, 'saleor', 'settings.py')
            if os.path.exists(settings_file):
                spec = importlib.util.spec_from_file_location('saleor.settings', settings_file)
                saleor_settings_module = importlib.util.module_from_spec(spec)
                
                # We need to load saleor first to make saleor.settings work
                saleor_init = os.path.join(site_packages, 'saleor', '__init__.py')
                if os.path.exists(saleor_init):
                    saleor_spec = importlib.util.spec_from_file_location('saleor', saleor_init)
                    saleor_module = importlib.util.module_from_spec(saleor_spec)
                    sys.modules['saleor'] = saleor_module
                    saleor_spec.loader.exec_module(saleor_module)
                
                spec.loader.exec_module(saleor_settings_module)
                sys.modules['saleor.settings'] = saleor_settings_module
                
                # Copy all uppercase attributes
                for attr_name in dir(saleor_settings_module):
                    if attr_name.isupper() and not attr_name.startswith('_'):
                        try:
                            globals()[attr_name] = getattr(saleor_settings_module, attr_name)
                        except (AttributeError, TypeError):
                            pass
            else:
                raise ImportError(f"Saleor settings.py not found at {settings_file}")
        else:
            raise ImportError("Could not find site-packages directory")
            
    except Exception as e2:
        # If all else fails, check if Saleor is even installed
        raise ImportError(
            f"Could not import Saleor settings. Original error: {e}. "
            f"Secondary attempt error: {e2}. "
            "Make sure Saleor is installed: pip install git+https://github.com/saleor/saleor.git"
        )

# Verify INSTALLED_APPS was imported
if 'INSTALLED_APPS' not in globals():
    raise ImportError(
        "INSTALLED_APPS not found after importing Saleor settings. "
        "The Saleor package may have a different settings structure or wasn't installed correctly."
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
