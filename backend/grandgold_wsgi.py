"""
Grand Gold WSGI entrypoint.

Why this exists:
- Railway/Gunicorn was started with `gunicorn wsgi:application`. If the working directory
  isn't what we think, Python might import a different `wsgi` module (or fail over in
  unexpected ways), causing our `grandgold_settings` + URLConf override to be ignored.
- Using a uniquely named module removes that ambiguity.
"""

import os
import sys

# Ensure backend directory is on sys.path
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Ensure our settings are used
# IMPORTANT: setdefault() will NOT override Railway-provided env vars.
# If Railway has DJANGO_SETTINGS_MODULE set (often to Saleor defaults), our URLConf/schema
# overrides will never be used. Force it here so runtime behavior is deterministic.
# #region agent log
_prev_settings = os.environ.get("DJANGO_SETTINGS_MODULE")
os.environ["DJANGO_SETTINGS_MODULE"] = "grandgold_settings"
print(f"🔍 [BOOT] grandgold_wsgi: DJANGO_SETTINGS_MODULE was {_prev_settings!r}, now {os.environ['DJANGO_SETTINGS_MODULE']!r}")
# #endregion

# Create application
from django.core.wsgi import get_wsgi_application  # noqa: E402

application = get_wsgi_application()


