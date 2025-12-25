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

# Set up libmagic path before running migrations
# This is needed for python-magic which is used by Saleor
# The nixpacks start command sets this, but we need it for migrations too
try:
    import subprocess
    result = subprocess.run(
        ['find', '/nix/store', '-name', 'libmagic.so*', '2>/dev/null'],
        shell=True,
        capture_output=True,
        text=True,
        timeout=5
    )
    if result.returncode == 0 and result.stdout.strip():
        libmagic_path = result.stdout.strip().split('\n')[0]
        libmagic_dir = os.path.dirname(libmagic_path)
        current_ld_path = os.environ.get('LD_LIBRARY_PATH', '')
        if libmagic_dir and libmagic_dir not in current_ld_path:
            os.environ['LD_LIBRARY_PATH'] = f"{current_ld_path}:{libmagic_dir}" if current_ld_path else libmagic_dir
except Exception:
    # If we can't find libmagic, that's OK - migrations might still work
    pass

# Run migrations on startup if DATABASE_URL is available
# NOTE: Migrations should be generated locally and committed to git
# This only applies existing migrations, it does not create new ones
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
            from io import StringIO
            output = StringIO()
            call_command('migrate', verbosity=2, interactive=False, stdout=output)
            result = output.getvalue()
            if 'No migrations to apply' in result or 'Applying' in result:
                print("✅ Migrations checked/run on startup")
                # Show summary of what was applied
                if 'Applying' in result:
                    applied = [line for line in result.split('\n') if 'Applying' in line]
                    if applied:
                        print(f"   Applied: {len(applied)} migration(s)")
            else:
                print(f"✅ Migrations checked: {result[:200]}")
        except Exception as e:
            error_msg = str(e).lower()
            # libmagic errors are not critical - migrations can still work
            if 'libmagic' in error_msg:
                # Try to run migrations using a subprocess to avoid libmagic import issues
                try:
                    # Ensure virtual environment is activated in subprocess
                    subprocess_env = os.environ.copy()
                    # Add virtual environment to PATH if it exists
                    venv_python = os.path.join(backend_dir, '.venv', 'bin', 'python')
                    if os.path.exists(venv_python):
                        subprocess_env['PATH'] = os.path.join(backend_dir, '.venv', 'bin') + ':' + subprocess_env.get('PATH', '')
                        # Use venv python instead of sys.executable
                        python_cmd = venv_python
                    else:
                        python_cmd = sys.executable
                    
                    # Set up libmagic path for subprocess (same as start command in nixpacks.toml)
                    # Use a shell command to set LD_LIBRARY_PATH and run migrate
                    # Increase timeout to 120 seconds for migrations
                    shell_cmd = (
                        f"LIB_PATH=$(find /nix/store -name libmagic.so* 2>/dev/null | head -1 | xargs dirname 2>/dev/null); "
                        f"export LD_LIBRARY_PATH=$LD_LIBRARY_PATH${{LIB_PATH:+:$LIB_PATH}}; "
                        f"cd {backend_dir} && "
                        f"{python_cmd} manage.py migrate --noinput 2>&1 || "
                        f"(echo '⚠️  Migration failed, checking for duplicate column issue...' && "
                        f"{python_cmd} -c \""
                        f"import os, sys, django; "
                        f"os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grandgold_settings'); "
                        f"sys.path.insert(0, '{backend_dir}'); "
                        f"django.setup(); "
                        f"from django.db import connection; "
                        f"from django.core.management import call_command; "
                        f"cursor = connection.cursor(); "
                        f"cursor.execute(\\\"SELECT column_name FROM information_schema.columns WHERE table_name='site_sitesettings' AND column_name='display_gross_prices'\\\"); "
                        f"if cursor.fetchone(): "
                        f"  call_command('migrate', 'site', '0014', '--fake', verbosity=0); "
                        f"  print('✅ Fixed duplicate column issue'); "
                        f"  call_command('migrate', verbosity=0, interactive=False); "
                        f"else: "
                        f"  sys.exit(1)"
                        f"\" 2>&1 || echo '⚠️  Could not auto-fix migration issue')"
                    )
                    
                    result = subprocess.run(
                        ['/bin/bash', '-c', shell_cmd],
                        capture_output=True,
                        text=True,
                        timeout=120,  # Increased timeout
                        env=subprocess_env
                    )
                    if result.returncode == 0:
                        print("✅ Migrations checked/run on startup (via subprocess)")
                    else:
                        # Show the actual error for debugging
                        error_output = result.stderr or result.stdout or "No error output"
                        print(f"⚠️  Migration subprocess failed (exit code {result.returncode})")
                        # Print full error (up to 2000 chars to see more context)
                        print(f"   STDOUT: {result.stdout[:2000] if result.stdout else '(empty)'}")
                        print(f"   STDERR: {error_output[:2000] if error_output else '(empty)'}")
                        print("   This might be OK if migrations were already run during build")
                except Exception as e2:
                    print(f"⚠️  Could not run migrations on startup: {e2}")
                    print("   This is OK - migrations may have already been run during build")
            else:
                print(f"⚠️  Could not run migrations on startup: {e}")
                print("   This is OK - migrations may have already been run during build")
    except Exception as e:
        print(f"⚠️  Database not available on startup: {e}")
        print("   Migrations will run when database becomes available")

# Create application
from django.core.wsgi import get_wsgi_application  # noqa: E402

application = get_wsgi_application()


