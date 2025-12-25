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
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "grandgold_settings")

# Create application
from django.core.wsgi import get_wsgi_application  # noqa: E402

application = get_wsgi_application()


