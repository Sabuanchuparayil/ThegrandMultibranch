"""
Django settings for Grand Gold & Diamonds project.

This module extends Saleor's default settings with our custom configurations.
We import from the installed Saleor package and then apply our extensions.
"""

import sys
import os
import json
import time

# #region agent log
def _log_msg(loc, msg, data, hyp):
    try:
        log_path = '/Users/apple/Desktop/Grand Gold/The grand-Multibranch/.cursor/debug.log'
        entry = {
            "timestamp": int(time.time() * 1000),
            "location": loc,
            "message": msg,
            "data": data,
            "sessionId": "debug-session",
            "runId": "initial",
            "hypothesisId": hyp
        }
        with open(log_path, 'a') as f:
            f.write(json.dumps(entry) + '\n')
    except:
        pass
# #endregion

# We need to import Saleor from the installed package, not our local saleor directory
# Our local backend/saleor/ directory is interfering with the import
# Strategy: Temporarily remove local saleor from sys.modules and force import from site-packages

# #region agent log
_log_msg('grandgold_settings.py:36', 'Starting Saleor import attempt', {'sys_path_length': len(sys.path), 'backend_dir_in_path': os.path.dirname(__file__) in sys.path}, 'A')
# #endregion

# Store and temporarily remove local saleor modules to force import from installed package
_local_saleor_modules = {}
for key in list(sys.modules.keys()):
    if key.startswith('saleor'):
        _local_saleor_modules[key] = sys.modules.pop(key)

try:
    # Now import from installed package (should be in site-packages)
    import importlib
    import importlib.util
    import site
    
    # Find site-packages that contains saleor
    site_packages_path = None
    for sp_path in site.getsitepackages():
        saleor_path = os.path.join(sp_path, 'saleor')
        if os.path.exists(saleor_path):
            site_packages_path = sp_path
            break
    
    # #region agent log
    _log_msg('grandgold_settings.py:53', 'Looking for installed Saleor', {'site_packages_path': site_packages_path, 'saleor_exists': os.path.exists(os.path.join(site_packages_path, 'saleor')) if site_packages_path else False}, 'A')
    # #endregion
    
    if site_packages_path:
        # Explicitly load from site-packages
        settings_file = os.path.join(site_packages_path, 'saleor', 'settings.py')
        if os.path.exists(settings_file):
            # Load saleor package first
            saleor_init = os.path.join(site_packages_path, 'saleor', '__init__.py')
            if os.path.exists(saleor_init):
                saleor_spec = importlib.util.spec_from_file_location('saleor', saleor_init)
                saleor_module = importlib.util.module_from_spec(saleor_spec)
                sys.modules['saleor'] = saleor_module
                saleor_spec.loader.exec_module(saleor_module)
            
            # Load settings module
            spec = importlib.util.spec_from_file_location('saleor.settings', settings_file)
            saleor_settings_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(saleor_settings_module)
            sys.modules['saleor.settings'] = saleor_settings_module
            
            # #region agent log
            _log_msg('grandgold_settings.py:70', 'Loaded from site-packages', {'has_INSTALLED_APPS': hasattr(saleor_settings_module, 'INSTALLED_APPS'), 'uppercase_count': len([a for a in dir(saleor_settings_module) if a.isupper()])}, 'A')
            # #endregion
            
            # Copy all uppercase attributes (Django settings)
            copied = 0
            for attr_name in dir(saleor_settings_module):
                if attr_name.isupper() and not attr_name.startswith('_'):
                    try:
                        globals()[attr_name] = getattr(saleor_settings_module, attr_name)
                        copied += 1
                    except (AttributeError, TypeError):
                        pass
            
            # #region agent log
            _log_msg('grandgold_settings.py:82', 'Copied attributes', {'copied_count': copied, 'INSTALLED_APPS_in_globals': 'INSTALLED_APPS' in globals()}, 'A')
            # #endregion
        else:
            raise ImportError(f"Saleor settings.py not found at {settings_file}")
    else:
        # Fallback: try direct import (might work if site-packages is in path correctly)
        from saleor.settings import *  # noqa: F403, F405
    
except ImportError as e:
    # #region agent log
    _log_msg('grandgold_settings.py:39', 'Direct import failed, trying fallback', {'error': str(e)}, 'B')
    # #endregion
    
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
        
        # #region agent log
        _log_msg('grandgold_settings.py:53', 'Found site-packages', {'site_packages': site_packages, 'saleor_exists': os.path.exists(os.path.join(site_packages, 'saleor')) if site_packages else False}, 'B')
        # #endregion
        
        if site_packages:
            # Load saleor.settings from site-packages explicitly
            settings_file = os.path.join(site_packages, 'saleor', 'settings.py')
            # #region agent log
            _log_msg('grandgold_settings.py:58', 'Checking settings file', {'settings_file': settings_file, 'exists': os.path.exists(settings_file)}, 'B')
            # #endregion
            
            if os.path.exists(settings_file):
                spec = importlib.util.spec_from_file_location('saleor.settings', settings_file)
                saleor_settings_module = importlib.util.module_from_spec(spec)
                
                # We need to load saleor first to make saleor.settings work
                saleor_init = os.path.join(site_packages, 'saleor', '__init__.py')
                # #region agent log
                _log_msg('grandgold_settings.py:66', 'Loading saleor module', {'saleor_init': saleor_init, 'exists': os.path.exists(saleor_init)}, 'B')
                # #endregion
                
                if os.path.exists(saleor_init):
                    saleor_spec = importlib.util.spec_from_file_location('saleor', saleor_init)
                    saleor_module = importlib.util.module_from_spec(saleor_spec)
                    sys.modules['saleor'] = saleor_module
                    saleor_spec.loader.exec_module(saleor_module)
                
                spec.loader.exec_module(saleor_settings_module)
                sys.modules['saleor.settings'] = saleor_settings_module
                
                # #region agent log
                _log_msg('grandgold_settings.py:77', 'Module loaded, checking attributes', {'has_INSTALLED_APPS': hasattr(saleor_settings_module, 'INSTALLED_APPS'), 'dir_attrs_count': len(dir(saleor_settings_module)), 'uppercase_attrs': [a for a in dir(saleor_settings_module) if a.isupper()][:10]}, 'C')
                # #endregion
                
                # Copy all uppercase attributes
                copied_count = 0
                for attr_name in dir(saleor_settings_module):
                    if attr_name.isupper() and not attr_name.startswith('_'):
                        try:
                            attr_value = getattr(saleor_settings_module, attr_name)
                            globals()[attr_name] = attr_value
                            copied_count += 1
                            if attr_name == 'INSTALLED_APPS':
                                # #region agent log
                                _log_msg('grandgold_settings.py:87', 'Copied INSTALLED_APPS', {'type': str(type(attr_value)), 'is_list': isinstance(attr_value, list)}, 'B')
                                # #endregion
                        except (AttributeError, TypeError) as copy_err:
                            # #region agent log
                            _log_msg('grandgold_settings.py:92', 'Failed to copy attribute', {'attr': attr_name, 'error': str(copy_err)}, 'D')
                            # #endregion
                            pass
                
                # #region agent log
                _log_msg('grandgold_settings.py:96', 'Finished copying attributes', {'copied_count': copied_count, 'INSTALLED_APPS_in_globals': 'INSTALLED_APPS' in globals()}, 'B')
                # #endregion
            else:
                raise ImportError(f"Saleor settings.py not found at {settings_file}")
        else:
            raise ImportError("Could not find site-packages directory")
            
    except Exception as e2:
        # #region agent log
        _log_msg('grandgold_settings.py:104', 'Fallback import also failed', {'error': str(e2)}, 'E')
        # #endregion
        
        # If all else fails, check if Saleor is even installed
        raise ImportError(
            f"Could not import Saleor settings. Original error: {e}. "
            f"Secondary attempt error: {e2}. "
            "Make sure Saleor is installed: pip install git+https://github.com/saleor/saleor.git"
        )

# #region agent log
_log_msg('grandgold_settings.py:113', 'Verifying INSTALLED_APPS', {'INSTALLED_APPS_in_globals': 'INSTALLED_APPS' in globals(), 'globals_uppercase': [k for k in globals().keys() if k.isupper() and not k.startswith('_')][:15]}, 'A')
# #endregion

# Verify INSTALLED_APPS was imported
if 'INSTALLED_APPS' not in globals():
    # #region agent log
    available_uppercase = [k for k in globals().keys() if k.isupper() and not k.startswith('_')][:20]
    # Try to get INSTALLED_APPS directly from the module if it exists there
    try:
        import saleor.settings as ss_check
        has_in_module = hasattr(ss_check, 'INSTALLED_APPS')
        module_path = getattr(ss_check, '__file__', 'unknown')
    except:
        has_in_module = False
        module_path = 'error_checking'
    
    _log_msg('grandgold_settings.py:160', 'INSTALLED_APPS not found - raising error', {'available_uppercase': available_uppercase, 'has_in_module': has_in_module, 'module_path': module_path}, 'E')
    # #endregion
    
    # Include debug info in error message for Railway logs
    raise ImportError(
        f"INSTALLED_APPS not found after importing Saleor settings. "
        f"Available uppercase globals: {available_uppercase}. "
        f"INSTALLED_APPS in module: {has_in_module}. "
        f"Module path: {module_path}. "
        f"The Saleor package may have a different settings structure or wasn't installed correctly."
    )

# #region agent log
_log_msg('grandgold_settings.py:125', 'INSTALLED_APPS found, extending', {'current_apps_count': len(INSTALLED_APPS) if isinstance(globals().get('INSTALLED_APPS'), list) else 'not_a_list'}, 'A')
# #endregion

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
