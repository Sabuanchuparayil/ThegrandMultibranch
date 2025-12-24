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
        # Use Railway-safe log path: try .cursor/debug.log first, then /tmp/debug.log
        log_path = os.path.join(os.path.dirname(__file__), '.cursor', 'debug.log')
        log_dir = os.path.dirname(log_path)
        if not os.path.exists(log_dir):
            log_path = '/tmp/debug.log'  # Fallback to /tmp on Railway
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
    except Exception as log_err:
        # Silently fail logging - don't break the import process
        pass
# #endregion

# We need to import Saleor from the installed package, not our local saleor directory
# Our local backend/saleor/ directory is interfering with the import
# Strategy: Temporarily remove local saleor from sys.modules and force import from site-packages

# #region agent log
backend_dir = os.path.dirname(__file__)
_log_msg('grandgold_settings.py:36', 'Starting Saleor import attempt', {
    'sys_path_length': len(sys.path),
    'backend_dir': backend_dir,
    'backend_dir_in_path': backend_dir in sys.path,
    'sys_path_first_5': sys.path[:5],
    'file_location': __file__
}, 'A')
# #endregion

# Store and temporarily remove local saleor modules to force import from installed package
_local_saleor_modules = {}
for key in list(sys.modules.keys()):
    if key.startswith('saleor'):
        _local_saleor_modules[key] = sys.modules.pop(key)

# Try simplest approach: temporarily prioritize site-packages in sys.path, then import
backend_dir = os.path.dirname(__file__)
_original_sys_path = list(sys.path)
direct_import_succeeded = False
try:
    # Reorder sys.path: put site-packages first, move /app to end
    site_packages_paths = [p for p in sys.path if 'site-packages' in p]
    app_paths = [p for p in sys.path if p == backend_dir or (p and backend_dir in p.replace('\\', '/'))]
    other_paths = [p for p in sys.path if p not in site_packages_paths and p not in app_paths]
    
    # New order: site-packages first, then others, then /app last
    sys.path = site_packages_paths + other_paths + app_paths
    
    # #region agent log
    _log_msg('grandgold_settings.py:58', 'Reordered sys.path for import', {
        'site_packages_paths': site_packages_paths,
        'app_paths': app_paths,
        'new_sys_path': sys.path[:5]
    }, 'E')
    # #endregion
    
    import saleor
    saleor_file = getattr(saleor, '__file__', None)
    saleor_path = getattr(saleor, '__path__', [None])[0] if hasattr(saleor, '__path__') else None
    saleor_location = saleor_file or saleor_path
    
    # #region agent log
    _log_msg('grandgold_settings.py:68', 'Direct import attempt', {
        'saleor_location': saleor_location,
        'saleor_file': saleor_file,
        'saleor_path': saleor_path,
        'is_site_packages': 'site-packages' in (saleor_location or '')
    }, 'E')
    # #endregion
    
    if saleor_location and 'site-packages' in saleor_location:
        # Saleor is installed correctly, use standard import
        from saleor import settings as saleor_settings_module
        
        # Copy all uppercase attributes
        for attr_name in dir(saleor_settings_module):
            if attr_name.isupper() and not attr_name.startswith('_'):
                try:
                    globals()[attr_name] = getattr(saleor_settings_module, attr_name)
                except (AttributeError, TypeError):
                    pass
        
        # Restore original sys.path
        sys.path = _original_sys_path
        
        # #region agent log
        _log_msg('grandgold_settings.py:88', 'Direct import succeeded', {
            'INSTALLED_APPS_in_globals': 'INSTALLED_APPS' in globals(),
            'saleor_location': saleor_location
        }, 'E')
        # #endregion
        
        # Success! Skip manual loading
        direct_import_succeeded = True
    else:
        # Restore original sys.path before falling through
        sys.path = _original_sys_path
        direct_import_succeeded = False
        raise ImportError(f"Saleor imported but location doesn't look like site-packages: {saleor_location}")
except (ImportError, Exception) as direct_import_error:
    # Restore original sys.path
    sys.path = _original_sys_path
    direct_import_succeeded = False
    # #region agent log
    _log_msg('grandgold_settings.py:99', 'Direct import failed, using manual loading', {
        'error': str(direct_import_error),
        'error_type': type(direct_import_error).__name__
    }, 'E')
    # #endregion

# Skip manual loading if direct import already succeeded
if 'INSTALLED_APPS' not in globals():
    try:
        # Now import from installed package (should be in site-packages)
        import importlib
        import importlib.util
        import site
    
        # Find site-packages that contains saleor
        # Try multiple methods to find site-packages
        site_packages_path = None
    
        # Method 1: site.getsitepackages()
        all_site_packages = site.getsitepackages()
    
        # #region agent log
        _log_msg('grandgold_settings.py:57', 'Method 1: site.getsitepackages()', {
        'all_site_packages': all_site_packages,
        'count': len(all_site_packages) if all_site_packages else 0
        }, 'A')
        # #endregion
    
        # Method 2: Check sys.path for site-packages
        # Include paths with 'site-packages' - even if they're in /app/.venv/ (that's the installed packages)
        # Only exclude /app/ paths that DON'T have site-packages (those are our local code)
        sys_site_packages = [p for p in sys.path if 'site-packages' in p]
    
        # #region agent log
        _log_msg('grandgold_settings.py:62', 'Method 2: sys.path filtering', {
        'sys_site_packages': sys_site_packages,
        'sys_path_all': sys.path,
        'filtered_count': len(sys_site_packages)
        }, 'B')
        # #endregion
    
        # Method 3: Try .venv directory explicitly (Railway uses .venv)
        backend_dir = os.path.dirname(__file__)
        venv_site_packages = os.path.join(backend_dir, '.venv', 'lib', 'python3.11', 'site-packages')
        venv_exists = os.path.exists(venv_site_packages)
        saleor_in_venv = os.path.exists(os.path.join(venv_site_packages, 'saleor')) if venv_exists else False
    
        # #region agent log
        _log_msg('grandgold_settings.py:70', 'Method 3: Direct venv check', {
        'backend_dir': backend_dir,
        'venv_site_packages': venv_site_packages,
        'venv_exists': venv_exists,
        'saleor_in_venv': saleor_in_venv
        }, 'C')
        # #endregion
    
        if venv_exists and saleor_in_venv:
            site_packages_path = venv_site_packages
    
        # Method 3b: Try /app/.venv directly (Railway root)
        app_venv_site_packages = '/app/.venv/lib/python3.11/site-packages'
        app_venv_exists = os.path.exists(app_venv_site_packages)
        saleor_in_app_venv = os.path.exists(os.path.join(app_venv_site_packages, 'saleor')) if app_venv_exists else False
    
        # #region agent log
        _log_msg('grandgold_settings.py:82', 'Method 3b: /app/.venv check', {
        'app_venv_site_packages': app_venv_site_packages,
        'app_venv_exists': app_venv_exists,
        'saleor_in_app_venv': saleor_in_app_venv
        }, 'C')
        # #endregion
    
        if app_venv_exists and saleor_in_app_venv and not site_packages_path:
            site_packages_path = app_venv_site_packages
    
        # Method 4: Try to find where saleor is actually installed
        # Check paths but EXCLUDE /app directory (that's our local code)
        checked_paths = []
        for check_path in sys_site_packages + (all_site_packages or []):
        if check_path and os.path.exists(check_path):
            # Skip /app directory - that's our local code, not installed packages
            normalized_path = check_path.replace('\\', '/')
            if '/app/' in normalized_path and 'site-packages' not in normalized_path:
                continue
            saleor_path = os.path.join(check_path, 'saleor')
            saleor_exists = os.path.exists(saleor_path)
            checked_paths.append({
                'path': check_path,
                'saleor_exists': saleor_exists,
                'normalized': normalized_path
            })
            if saleor_exists:
                # Verify this is NOT our local saleor directory
                local_saleor = os.path.join(backend_dir, 'saleor')
                if os.path.exists(local_saleor):
                    try:
                        is_local = os.path.samefile(saleor_path, local_saleor)
                    except (OSError, ValueError):
                        # Can't compare (different filesystems or one doesn't exist), check by path
                        is_local = os.path.abspath(saleor_path) == os.path.abspath(local_saleor)
                else:
                    is_local = False
                
                if not is_local:
                    site_packages_path = check_path
                    break
    
        # #region agent log
        _log_msg('grandgold_settings.py:100', 'Method 4: Iterating paths', {
        'checked_paths': checked_paths[:10],
        'found_site_packages': site_packages_path
        }, 'B')
        # #endregion
    
        # #region agent log
        _log_msg('grandgold_settings.py:115', 'Summary: Looking for installed Saleor', {
        'site_getsitepackages': all_site_packages,
        'sys_site_packages': sys_site_packages,
        'sys_path': sys.path,
        'found_site_packages_path': site_packages_path,
        'saleor_exists': os.path.exists(os.path.join(site_packages_path, 'saleor')) if site_packages_path else False,
        'python_version': sys.version
        }, 'A')
        # #endregion
    
        if site_packages_path:
        # Explicitly load from site-packages
        saleor_dir = os.path.join(site_packages_path, 'saleor')
        
        # Check different possible locations for Saleor settings
        settings_file = os.path.join(saleor_dir, 'settings.py')
        settings_package = os.path.join(saleor_dir, 'settings')
        
        # #region agent log
        _log_msg('grandgold_settings.py:66', 'Checking Saleor structure', {
            'saleor_dir_exists': os.path.exists(saleor_dir),
            'settings_py_exists': os.path.exists(settings_file),
            'settings_package_exists': os.path.isdir(settings_package),
            'saleor_contents': os.listdir(saleor_dir)[:10] if os.path.exists(saleor_dir) else []
        }, 'A')
        # #endregion
        
        saleor_settings_module = None
        
        # Load saleor package first
        saleor_init = os.path.join(saleor_dir, '__init__.py')
        if os.path.exists(saleor_init):
            saleor_spec = importlib.util.spec_from_file_location('saleor', saleor_init)
            saleor_module = importlib.util.module_from_spec(saleor_spec)
            sys.modules['saleor'] = saleor_module
            saleor_spec.loader.exec_module(saleor_module)
        
        # Try settings.py first
        if os.path.exists(settings_file):
            spec = importlib.util.spec_from_file_location('saleor.settings', settings_file)
            saleor_settings_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(saleor_settings_module)
            sys.modules['saleor.settings'] = saleor_settings_module
        # Try settings package with __init__.py
        elif os.path.isdir(settings_package):
            settings_init = os.path.join(settings_package, '__init__.py')
            if os.path.exists(settings_init):
                spec = importlib.util.spec_from_file_location('saleor.settings', settings_init)
                saleor_settings_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(saleor_settings_module)
                sys.modules['saleor.settings'] = saleor_settings_module
        
        if saleor_settings_module:
            # #region agent log
            _log_msg('grandgold_settings.py:95', 'Loaded settings module', {
                'has_INSTALLED_APPS': hasattr(saleor_settings_module, 'INSTALLED_APPS'),
                'all_attrs': len(dir(saleor_settings_module)),
                'uppercase_attrs': [a for a in dir(saleor_settings_module) if a.isupper()][:15]
            }, 'A')
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
            _log_msg('grandgold_settings.py:109', 'Copied attributes', {'copied_count': copied, 'INSTALLED_APPS_in_globals': 'INSTALLED_APPS' in globals()}, 'A')
            # #endregion
        else:
            raise ImportError(f"Saleor settings not found at {settings_file} or {settings_package}")
        else:
        # Try to find Saleor in sys.path directly as fallback
        # BUT exclude local /app/saleor directory - only accept site-packages locations
        saleor_found_path = None
        backend_dir = os.path.dirname(__file__)
        local_saleor = os.path.join(backend_dir, 'saleor')
        
        # #region agent log
        _log_msg('grandgold_settings.py:237', 'Fallback: searching sys.path', {
            'sys_path': sys.path,
            'backend_dir': backend_dir,
            'local_saleor': local_saleor,
            'local_saleor_exists': os.path.exists(local_saleor)
        }, 'D')
        # #endregion
        
        for check_path in sys.path:
            if check_path and os.path.exists(check_path):
                saleor_check = os.path.join(check_path, 'saleor')
                if os.path.exists(saleor_check):
                    # CRITICAL: Exclude local saleor directory
                    # Check if this is NOT our local saleor directory
                    normalized_check = os.path.abspath(saleor_check).replace('\\', '/')
                    normalized_local = os.path.abspath(local_saleor).replace('\\', '/') if os.path.exists(local_saleor) else None
                    
                    # CRITICAL: Only accept paths that contain 'site-packages'
                    # This ensures we never accidentally use the local /app/saleor directory
                    is_site_packages = 'site-packages' in check_path
                    
                    # #region agent log
                    _log_msg('grandgold_settings.py:252', 'Checking path in fallback', {
                        'check_path': check_path,
                        'saleor_check': saleor_check,
                        'is_site_packages': is_site_packages,
                        'normalized_check': normalized_check,
                        'normalized_local': normalized_local
                    }, 'D')
                    # #endregion
                    
                    if is_site_packages:
                        saleor_found_path = check_path
                        break
        
        if not saleor_found_path:
            # Final check: try direct import to see what error we get
            try:
                import saleor
                saleor_location = getattr(saleor, '__file__', None) or (getattr(saleor, '__path__', [None])[0] if hasattr(saleor, '__path__') else None)
                raise ImportError(
                    f"Could not find site-packages directory containing Saleor. "
                    f"site.getsitepackages(): {all_site_packages}. "
                    f"sys.path site-packages: {sys_site_packages}. "
                    f"Saleor module location: {saleor_location}. "
                    f"Saleor may not be installed correctly. Check Railway build logs."
                )
            except ImportError:
                raise ImportError(
                    f"Could not find site-packages directory containing Saleor. "
                    f"site.getsitepackages(): {all_site_packages}. "
                    f"sys.path site-packages: {sys_site_packages}. "
                    f"sys.path: {sys.path[:10]}. "
                    f"Saleor is not installed. Check Railway build logs for installation errors."
                )
        else:
            # Found in sys.path, continue loading
            site_packages_path = saleor_found_path
            saleor_dir = os.path.join(site_packages_path, 'saleor')
            settings_file = os.path.join(saleor_dir, 'settings.py')
            settings_package = os.path.join(saleor_dir, 'settings')
            
            # Load saleor package first
            saleor_init = os.path.join(saleor_dir, '__init__.py')
            if os.path.exists(saleor_init):
                saleor_spec = importlib.util.spec_from_file_location('saleor', saleor_init)
                saleor_module = importlib.util.module_from_spec(saleor_spec)
                sys.modules['saleor'] = saleor_module
                saleor_spec.loader.exec_module(saleor_module)
            
            saleor_settings_module = None
            if os.path.exists(settings_file):
                spec = importlib.util.spec_from_file_location('saleor.settings', settings_file)
                saleor_settings_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(saleor_settings_module)
                sys.modules['saleor.settings'] = saleor_settings_module
            elif os.path.isdir(settings_package):
                settings_init = os.path.join(settings_package, '__init__.py')
                if os.path.exists(settings_init):
                    spec = importlib.util.spec_from_file_location('saleor.settings', settings_init)
                    saleor_settings_module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(saleor_settings_module)
                    sys.modules['saleor.settings'] = saleor_settings_module
            
            if saleor_settings_module:
                for attr_name in dir(saleor_settings_module):
                    if attr_name.isupper() and not attr_name.startswith('_'):
                        try:
                            globals()[attr_name] = getattr(saleor_settings_module, attr_name)
                        except (AttributeError, TypeError):
                            pass
            else:
                raise ImportError(f"Saleor settings not found at {settings_file} or {settings_package}")
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
                # #region agent log
                _log_msg('grandgold_settings.py:307', 'Fallback: site-packages not found', {
                    'site_getsitepackages': site.getsitepackages(),
                    'sys_path': sys.path,
                    'backend_dir': os.path.dirname(__file__),
                    'app_venv_exists': os.path.exists('/app/.venv/lib/python3.11/site-packages'),
                    'saleor_in_app_venv': os.path.exists('/app/.venv/lib/python3.11/site-packages/saleor') if os.path.exists('/app/.venv/lib/python3.11/site-packages') else False
                }, 'E')
                # #endregion
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

# WSGI Application
# Railway's nixpacks requires this setting to find the WSGI application
WSGI_APPLICATION = 'wsgi.application'

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
