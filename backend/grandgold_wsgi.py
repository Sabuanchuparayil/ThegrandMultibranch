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

# CRITICAL: Set LD_LIBRARY_PATH for libmagic BEFORE any imports
# This must happen before Django or Saleor imports, as they may trigger libmagic usage
try:
    import subprocess
    result = subprocess.run(
        'find /nix/store -name libmagic.so* 2>/dev/null | head -1 | xargs dirname 2>/dev/null',
        shell=True,
        capture_output=True,
        text=True,
        timeout=3
    )
    if result.returncode == 0 and result.stdout.strip():
        libmagic_dir = result.stdout.strip()
        current_ld_path = os.environ.get('LD_LIBRARY_PATH', '')
        if libmagic_dir and libmagic_dir not in current_ld_path:
            os.environ['LD_LIBRARY_PATH'] = f"{current_ld_path}:{libmagic_dir}" if current_ld_path else libmagic_dir
            print(f"🔍 [BOOT] grandgold_wsgi: Set LD_LIBRARY_PATH={libmagic_dir}")
except Exception as e:
    # If we can't find libmagic, that's OK - it might be set by the start command
    pass

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
        # Use subprocess to run migrations to avoid django.setup() reentrant issues
        # This prevents "populate() isn't reentrant" errors when Django loads the WSGI app
        # Ensure virtual environment is activated in subprocess
        subprocess_env = os.environ.copy()
        # Add virtual environment to PATH if it exists
        venv_python = os.path.join(backend_dir, '.venv', 'bin', 'python')
        if os.path.exists(venv_python):
            subprocess_env['PATH'] = os.path.join(backend_dir, '.venv', 'bin') + ':' + subprocess_env.get('PATH', '')
            python_cmd = venv_python
        else:
            python_cmd = sys.executable
        
        # Set up libmagic path for subprocess (same as start command in nixpacks.toml)
        # Use smart_migrate.py which handles problematic migrations gracefully
        shell_cmd = (
            f"LIB_PATH=$(find /nix/store -name libmagic.so* 2>/dev/null | head -1 | xargs dirname 2>/dev/null); "
            f"export LD_LIBRARY_PATH=$LD_LIBRARY_PATH${{LIB_PATH:+:$LIB_PATH}}; "
            f"cd {backend_dir} && "
            f"{python_cmd} smart_migrate.py 2>&1"
        )
        
        result = subprocess.run(
            ['/bin/bash', '-c', shell_cmd],
            capture_output=True,
            text=True,
            timeout=180,  # Increased timeout for smart migration
            env=subprocess_env
        )
        if result.returncode == 0:
            print("✅ Migrations checked/run on startup (via subprocess)")
            # Print a short tail of the migration output so Railway logs show what actually happened
            if result.stdout:
                tail = result.stdout[-4000:]
                print("----- smart_migrate.py output (tail) -----")
                print(tail)
                print("----- end smart_migrate.py output -----")
        else:
            # Show the actual error for debugging
            error_output = result.stderr or result.stdout or "No error output"
            print(f"⚠️  Migration subprocess failed (exit code {result.returncode})")
            # Print a tail of stdout/stderr to capture the actual failure cause (often near the end)
            if result.stdout:
                print("----- smart_migrate.py STDOUT (tail) -----")
                print(result.stdout[-6000:])
                print("----- end smart_migrate.py STDOUT -----")
            if error_output:
                print("----- smart_migrate.py STDERR (tail) -----")
                print(error_output[-6000:])
                print("----- end smart_migrate.py STDERR -----")
            print("   This might be OK if migrations were already run during build")
    except Exception as e:
        error_msg = str(e).lower()
        if 'database' in error_msg or 'connection' in error_msg:
            print(f"⚠️  Database not available on startup: {e}")
            print("   Migrations will run when database becomes available")
        else:
            print(f"⚠️  Could not run migrations on startup: {e}")
            print("   This is OK - migrations may have already been run during build")

# Create application
from django.core.wsgi import get_wsgi_application  # noqa: E402

application = get_wsgi_application()


