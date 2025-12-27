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

# Ensure only one gunicorn worker runs startup DB tasks (migrations/repair scripts).
# Without this, multiple workers can race creating the same permissions/tables and crash with
# "duplicate key value violates unique constraint" or "relation already exists".
def _acquire_startup_lock():
    lock_path = "/tmp/grandgold_startup.lock"
    try:
        import fcntl  # Unix-only (Railway is Linux)

        fd = os.open(lock_path, os.O_CREAT | os.O_RDWR, 0o644)
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return fd
        except BlockingIOError:
            try:
                os.close(fd)
            except Exception:
                pass
            return None
    except Exception:
        # If we can't lock for any reason, fall back to running (best effort).
        return None

def _release_startup_lock(fd):
    if fd is None:
        return
    try:
        import fcntl

        fcntl.flock(fd, fcntl.LOCK_UN)
    except Exception:
        pass
    try:
        os.close(fd)
    except Exception:
        pass

def _should_run_startup_tasks():
    """
    Run DB startup tasks at most once per container boot.
    Gunicorn spawns multiple workers; we must avoid each worker running migrations.
    """
    return not os.path.exists("/tmp/grandgold_startup.done")

def _mark_startup_tasks_done():
    try:
        with open("/tmp/grandgold_startup.done", "w") as f:
            f.write("done\n")
    except Exception:
        pass

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
    _lock_fd = None
    if not _should_run_startup_tasks():
        print("ℹ️  Startup DB tasks already completed for this container; skipping.")
    else:
        _lock_fd = _acquire_startup_lock()
        if _lock_fd is None:
            print("ℹ️  Startup DB tasks already running in another worker; skipping migrations/repair in this worker.")
        else:
            # Re-check after acquiring lock to avoid a race between workers.
            if not _should_run_startup_tasks():
                print("ℹ️  Startup DB tasks already completed by another worker; skipping.")
                _release_startup_lock(_lock_fd)
                _lock_fd = None
            else:
                print("🔒 Acquired startup lock; running DB repair + migrations once.")
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
        
        if _lock_fd is not None:
            # Set up libmagic path for subprocess (same as start command in nixpacks.toml)
            # FIRST: Ensure critical Saleor tables exist (e.g. product_productchannellisting)
            # This fixes GraphQL 400 errors from missing tables
            try:
                ensure_tables_script = os.path.join(backend_dir, 'ensure_saleor_tables.py')
                if os.path.exists(ensure_tables_script):
                    print("----- Running ensure_saleor_tables.py -----")
                    shell_cmd = (
                        f"LIB_PATH=$(find /nix/store -name libmagic.so* 2>/dev/null | head -1 | xargs dirname 2>/dev/null); "
                        f"export LD_LIBRARY_PATH=$LD_LIBRARY_PATH${{LIB_PATH:+:$LIB_PATH}}; "
                        f"cd {backend_dir} && "
                        f"{python_cmd} ensure_saleor_tables.py 2>&1"
                    )
                    result = subprocess.run(
                        ['/bin/bash', '-c', shell_cmd],
                        capture_output=True,
                        text=True,
                        timeout=60,
                        env=subprocess_env,
                    )
                    if result.returncode == 0:
                        print("✅ ensure_saleor_tables.py completed successfully")
                        if result.stdout:
                            print(result.stdout)
                    else:
                        print(f"⚠️  ensure_saleor_tables.py had issues (exit code {result.returncode})")
                        if result.stdout:
                            print(f"STDOUT: {result.stdout}")
                        if result.stderr:
                            print(f"STDERR: {result.stderr}")
            except subprocess.TimeoutExpired:
                print("⚠️  ensure_saleor_tables.py timed out")
            except Exception as e:
                print(f"⚠️  Failed to run ensure_saleor_tables.py: {e}")
            
            # SECOND: Ensure ALL critical columns exist (comprehensive fix)
            # This fixes GraphQL query errors for missing columns
            try:
                # Try comprehensive fix first, fallback to old fix if needed
                fix_script = os.path.join(backend_dir, 'fix_all_product_columns.py')
                if not os.path.exists(fix_script):
                    fix_script = os.path.join(backend_dir, 'fix_product_search_document.py')
                
                if os.path.exists(fix_script):
                    script_name = os.path.basename(fix_script)
                    print(f"----- Running {script_name} -----")
                    # Set up libmagic path for subprocess
                    script_name_only = os.path.basename(fix_script)
                    shell_cmd = (
                        f"LIB_PATH=$(find /nix/store -name libmagic.so* 2>/dev/null | head -1 | xargs dirname 2>/dev/null); "
                        f"export LD_LIBRARY_PATH=$LD_LIBRARY_PATH${{LIB_PATH:+:$LIB_PATH}}; "
                        f"cd {backend_dir} && "
                        f"{python_cmd} {script_name_only} 2>&1"
                    )
                    result = subprocess.run(
                        ['/bin/bash', '-c', shell_cmd],
                        capture_output=True,
                        text=True,
                        timeout=30,
                        env=subprocess_env
                    )
                    if result.returncode == 0:
                        print(f"✅ {script_name} completed successfully")
                        if result.stdout:
                            print(result.stdout[-1000:])  # Show last 1000 chars of output
                    else:
                        print(f"⚠️  {script_name} had issues (exit code {result.returncode})")
                        if result.stderr:
                            print(f"STDERR: {result.stderr[:500]}")
                        if result.stdout:
                            print(f"STDOUT: {result.stdout[:500]}")
            except Exception as e:
                print(f"⚠️  Could not run product column fix: {e}")

            # Use smart_migrate.py which handles problematic migrations gracefully
            # Ensure both libmagic and libstdc++ are discoverable for optional deps (e.g. grpc).
            shell_cmd = (
                "LIBMAGIC_DIR=$(find /nix/store -name libmagic.so* 2>/dev/null | head -1 | xargs dirname 2>/dev/null); "
                "LIBSTDCXX_DIR=$(find /nix/store -name libstdc++.so.6 2>/dev/null | head -1 | xargs dirname 2>/dev/null); "
                "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH${LIBMAGIC_DIR:+:$LIBMAGIC_DIR}${LIBSTDCXX_DIR:+:$LIBSTDCXX_DIR}; "
                f"cd {backend_dir} && "
                f"{python_cmd} smart_migrate.py 2>&1"
            )

            result = subprocess.run(
                ['/bin/bash', '-c', shell_cmd],
                capture_output=True,
                text=True,
                timeout=600,  # Saleor migrations can take several minutes on first boot
                env=subprocess_env,
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
            
            # THIRD: Create superuser and generate auth token if needed
            # This ensures admin user is always available after migrations
            try:
                create_user_script = os.path.join(backend_dir, 'create_superuser_if_needed.py')
                if os.path.exists(create_user_script):
                    print("----- Running create_superuser_if_needed.py -----")
                    shell_cmd = (
                        f"LIB_PATH=$(find /nix/store -name libmagic.so* 2>/dev/null | head -1 | xargs dirname 2>/dev/null); "
                        f"export LD_LIBRARY_PATH=$LD_LIBRARY_PATH${{LIB_PATH:+:$LIB_PATH}}; "
                        f"cd {backend_dir} && "
                        f"{python_cmd} create_superuser_if_needed.py 2>&1"
                    )
                    result = subprocess.run(
                        ['/bin/bash', '-c', shell_cmd],
                        capture_output=True,
                        text=True,
                        timeout=60,
                        env=subprocess_env,
                    )
                    if result.returncode == 0:
                        print("✅ create_superuser_if_needed.py completed successfully")
                        if result.stdout:
                            # Print the full output to show the token
                            print(result.stdout)
                    else:
                        print(f"⚠️  create_superuser_if_needed.py had issues (exit code {result.returncode})")
                        if result.stdout:
                            print(f"STDOUT: {result.stdout}")
                        if result.stderr:
                            print(f"STDERR: {result.stderr}")
            except subprocess.TimeoutExpired:
                print("⚠️  create_superuser_if_needed.py timed out")
            except Exception as e:
                print(f"⚠️  Failed to run create_superuser_if_needed.py: {e}")
    except Exception as e:
        error_msg = str(e).lower()
        if 'database' in error_msg or 'connection' in error_msg:
            print(f"⚠️  Database not available on startup: {e}")
            print("   Migrations will run when database becomes available")
        else:
            print(f"⚠️  Could not run migrations on startup: {e}")
            print("   This is OK - migrations may have already been run during build")
    finally:
        # Mark as done even if something failed so we don't spam/run repeatedly per worker.
        if _lock_fd is not None:
            _mark_startup_tasks_done()
        _release_startup_lock(_lock_fd)

# Create application
from django.core.wsgi import get_wsgi_application  # noqa: E402

application = get_wsgi_application()


