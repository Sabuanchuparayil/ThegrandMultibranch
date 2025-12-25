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

# Run migrations on startup if DATABASE_URL is available
# This ensures migrations run even if they didn't run during build
if os.environ.get('DATABASE_URL'):
    try:
        # Import Django setup first
        import django
        django.setup()
        from django.db import connection
        from django.core.management import call_command
        
        # Check if we can connect to the database
        connection.ensure_connection()
        # Try to run migrations (will skip if already applied)
        try:
            call_command('migrate', verbosity=0, interactive=False)
            print("✅ Migrations checked/run on startup")
        except Exception as e:
            print(f"⚠️  Could not run migrations on startup: {e}")
            print("   This is OK - migrations may have already been run during build")
    except Exception as e:
        print(f"⚠️  Database not available on startup: {e}")
        print("   Migrations will run when database becomes available")

# Create application
from django.core.wsgi import get_wsgi_application  # noqa: E402

application = get_wsgi_application()


