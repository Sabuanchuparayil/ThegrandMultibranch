"""
WSGI config for Grand Gold & Diamonds project.

This file creates the WSGI application using our custom settings that extend Saleor.
"""

import os
import sys
import json
import time

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

