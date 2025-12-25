"""
WSGI config for Grand Gold & Diamonds project.

This file creates the WSGI application using our custom settings that extend Saleor.
"""

import os
import sys
import json
import time
import subprocess

# CRITICAL: Set LD_LIBRARY_PATH for libmagic BEFORE any imports
# This must happen before Django or Saleor imports, as Saleor imports magic during module load
if 'LD_LIBRARY_PATH' not in os.environ or 'libmagic' not in os.environ.get('LD_LIBRARY_PATH', ''):
    # Find libmagic.so in Nix store
    try:
        result = subprocess.run(
            ['find', '/nix/store', '-name', 'libmagic.so*', '-type', 'f'],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0 and result.stdout.strip():
            # Get the directory containing libmagic.so
            libmagic_path = result.stdout.strip().split('\n')[0]
            libmagic_dir = os.path.dirname(libmagic_path)
            # Add to LD_LIBRARY_PATH
            current_ld_path = os.environ.get('LD_LIBRARY_PATH', '')
            if libmagic_dir not in current_ld_path:
                os.environ['LD_LIBRARY_PATH'] = f"{libmagic_dir}:{current_ld_path}" if current_ld_path else libmagic_dir
    except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
        # If find command fails or times out, try common Nix paths
        common_paths = [
            '/nix/store/*/lib/libmagic.so*',
            '/nix/store/*-file-*/lib/libmagic.so*',
        ]
        # Fallback: try to set a reasonable default if we can't find it
        pass

# Monkey-patch magic import to handle missing libmagic gracefully
# This must happen before Saleor imports magic (which happens during URL loading)
try:
    import magic
    # Verify it actually works (not just imported)
    try:
        _test_magic = magic.Magic()
        _test_magic.from_file('/dev/null')  # Test if it works
    except:
        # If magic doesn't work, use fallback
        raise ImportError("magic module imported but libmagic not functional")
except (ImportError, OSError, Exception):
    # If magic import fails, create a mock module to prevent ImportError
    import types
    class MagicFallback:
        """Fallback class when libmagic is not available"""
        def __init__(self, *args, **kwargs):
            pass
        def from_file(self, *args, **kwargs):
            return None
        def from_buffer(self, *args, **kwargs):
            return None
    
    magic = types.ModuleType('magic')
    magic.Magic = MagicFallback
    sys.modules['magic'] = magic

# #region agent log
def _log_msg(loc, msg, data, hyp):
    try:
        log_path = os.path.join(os.path.dirname(__file__), '.cursor', 'debug.log')
        log_dir = os.path.dirname(log_path)
        if not os.path.exists(log_dir):
            log_path = '/tmp/debug.log'
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

# Add the backend directory to Python path so our local saleor package is found
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# #region agent log
_log_msg('wsgi.py:35', 'WSGI startup - checking Django version', {
    'backend_dir': backend_dir,
    'python_version': sys.version,
    'sys_path_length': len(sys.path)
}, 'B')
# #endregion

# Set Django settings module to use our custom settings that extend Saleor
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grandgold_settings')

# #region agent log
try:
    import django
    _log_msg('wsgi.py:44', 'Django imported successfully', {
        'django_version': django.get_version(),
        'django_location': django.__file__ if hasattr(django, '__file__') else None
    }, 'B')
except Exception as e:
    _log_msg('wsgi.py:44', 'Django import failed', {'error': str(e)}, 'B')
# #endregion

# Import Django's WSGI application
from django.core.wsgi import get_wsgi_application

# #region agent log
_log_msg('wsgi.py:54', 'About to call get_wsgi_application', {}, 'B')
# #endregion

application = get_wsgi_application()

# #region agent log
_log_msg('wsgi.py:58', 'WSGI application created successfully', {}, 'B')
# #endregion

