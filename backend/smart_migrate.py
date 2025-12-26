#!/usr/bin/env python3
"""
Smart migration script that handles problematic migrations gracefully.
Skips migrations that fail due to missing tables/columns and continues with others.
"""
import os
import sys

# During migrations we don't need Saleor plugins (and some optional plugins pull in heavy deps
# like google-cloud-pubsub/grpc which can fail in minimal containers). Disable them.
os.environ.setdefault("GG_DISABLE_SALEOR_PLUGINS", "1")

# Ensure native libs are discoverable (grpc can require libstdc++ at import time).
try:
    import subprocess

    libstdcxx_dir = (
        subprocess.run(
            "find /nix/store -name libstdc++.so.6 2>/dev/null | head -1 | xargs dirname 2>/dev/null",
            shell=True,
            capture_output=True,
            text=True,
            timeout=3,
        ).stdout.strip()
    )
    if libstdcxx_dir:
        current = os.environ.get("LD_LIBRARY_PATH", "")
        if libstdcxx_dir not in current:
            os.environ["LD_LIBRARY_PATH"] = f"{current}:{libstdcxx_dir}" if current else libstdcxx_dir
except Exception:
    pass

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grandgold_settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

django.setup()

import json
import time

from django.core.management import call_command
from django.db import connection, transaction
from django.db.utils import OperationalError, ProgrammingError

def patch_create_permissions_ignore_duplicates():
    """
    Some environments can end up partially migrated, and post_migrate permission creation can crash with:
      IntegrityError: duplicate key value violates unique constraint auth_permission_content_type_id_codename_..._uniq

    This should be safe to ignore (permission already exists) and should NOT block schema migrations.
    """
    try:
        from django.contrib.auth import management as auth_management
        from django.db.models.signals import post_migrate
        from django.db import IntegrityError

        orig = auth_management.create_permissions

        def safe_create_permissions(*args, **kwargs):
            try:
                return orig(*args, **kwargs)
            except IntegrityError as e:
                msg = str(e)
                if "auth_permission_content_type_id_codename" in msg:
                    print(f"⚠️  Ignoring duplicate permission IntegrityError: {msg}")
                    _log(
                        "smart_migrate.py:patch_create_permissions",
                        "Ignored duplicate permission IntegrityError",
                        {"error": msg},
                        "H21",
                    )
                    return None
                raise

        # Replace the receiver connected by django.contrib.auth so our wrapper is actually used.
        try:
            post_migrate.disconnect(
                receiver=orig,
                dispatch_uid="django.contrib.auth.management.create_permissions",
            )
        except Exception:
            pass
        post_migrate.connect(
            receiver=safe_create_permissions,
            dispatch_uid="django.contrib.auth.management.create_permissions",
        )

        # Keep module attribute consistent for any late imports.
        auth_management.create_permissions = safe_create_permissions
        _log(
            "smart_migrate.py:patch_create_permissions",
            "Patched create_permissions to ignore duplicate permission IntegrityError",
            {},
            "H21",
        )
        return True
    except Exception as e:
        _log(
            "smart_migrate.py:patch_create_permissions",
            "Failed patching create_permissions",
            {"error": str(e), "error_type": type(e).__name__},
            "H21",
        )
        return False

def _log(location, message, data, hypothesis_id="H7"):
    try:
        log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".cursor", "debug.log")
        entry = {
            "sessionId": "debug-session",
            "runId": "debug-run2",
            "hypothesisId": hypothesis_id,
            "location": location,
            "message": message,
            "data": data,
            "timestamp": int(time.time() * 1000),
        }
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        with open(log_path, "a") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception:
        pass

def ensure_postgres_extensions():
    """
    Saleor relies on some PostgreSQL extensions for search / indexing.
    If they are missing, migrations (especially `product`) can fail or later queries can break.
    """
    # #region agent log
    _log(
        "smart_migrate.py:ensure_postgres_extensions:entry",
        "Ensuring required PostgreSQL extensions",
        {"hypothesisId": "H18"},
        "H18",
    )
    # #endregion
    extensions = ["pg_trgm", "unaccent", "btree_gin"]
    ok = []
    failed = []
    try:
        with connection.cursor() as cursor:
            for ext in extensions:
                try:
                    cursor.execute(f"CREATE EXTENSION IF NOT EXISTS {ext};")
                    ok.append(ext)
                except Exception as e:
                    failed.append({"ext": ext, "error": str(e), "error_type": type(e).__name__})
        if failed:
            print(f"⚠️  Could not enable some PostgreSQL extensions: {failed}")
        else:
            print(f"✅ PostgreSQL extensions ensured: {ok}")
        _log(
            "smart_migrate.py:ensure_postgres_extensions:result",
            "PostgreSQL extensions ensured",
            {"ok": ok, "failed": failed, "hypothesisId": "H18"},
            "H18",
        )
        return len(failed) == 0
    except Exception as e:
        _log(
            "smart_migrate.py:ensure_postgres_extensions:exception",
            "Failed ensuring PostgreSQL extensions",
            {"error": str(e), "error_type": type(e).__name__, "hypothesisId": "H18"},
            "H18",
        )
        print(f"⚠️  Failed ensuring PostgreSQL extensions: {e}")
        return False

def check_table_exists(table_name):
    """Check if a table exists in the database"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = %s
            );
        """, [table_name])
        return cursor.fetchone()[0]

def check_column_exists(table_name, column_name):
    """Check if a column exists in a table"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.columns 
                WHERE table_schema = 'public' 
                AND table_name = %s 
                AND column_name = %s
            );
        """, [table_name, column_name])
        return cursor.fetchone()[0]

def ensure_saleor_channel_tables():
    """
    Products queries require Saleor Channels. If `channel_channel` is missing, try to migrate the `channel` app.
    """
    try:
        if check_table_exists("channel_channel"):
            _log("smart_migrate.py:ensure_channel", "channel_channel table exists", {}, "H14")
            return True

        print("⚠️  channel_channel missing; attempting to migrate channel app...")
        _log("smart_migrate.py:ensure_channel", "channel_channel missing; migrating channel app", {}, "H14")
        try:
            # Try normal migrate first
            call_command("migrate", "channel", verbosity=2, interactive=False)
        except Exception as e:
            # Try fake-initial as a recovery path if tables partially exist / migration graph mismatch
            print(f"⚠️  channel migrate failed, retrying with --fake-initial: {e}")
            _log(
                "smart_migrate.py:ensure_channel",
                "channel migrate failed; retrying fake_initial",
                {"error": str(e), "error_type": type(e).__name__},
                "H14",
            )
            try:
                call_command("migrate", "channel", verbosity=2, interactive=False, fake_initial=True)
            except Exception as e2:
                print(f"❌ channel migrate (fake-initial) failed: {e2}")
                _log(
                    "smart_migrate.py:ensure_channel",
                    "channel migrate failed",
                    {"error": str(e2), "error_type": type(e2).__name__},
                    "H14",
                )
                # Fall through to schema_editor create_model fallback
                pass
        except Exception as e:
            _log(
                "smart_migrate.py:ensure_channel",
                "channel migrate failed",
                {"error": str(e), "error_type": type(e).__name__},
                "H14",
            )
            # Fall through to schema_editor create_model fallback
            pass

        ok = check_table_exists("channel_channel")
        if not ok:
            print("⚠️  channel_channel still missing; attempting schema_editor.create_model(Channel) fallback...")
            try:
                from saleor.channel.models import Channel  # noqa: WPS433
                from django.db import connection as _conn

                with _conn.schema_editor() as schema_editor:
                    schema_editor.create_model(Channel)
                ok = check_table_exists("channel_channel")
                if ok:
                    # Ensure at least one channel exists so products queries can resolve
                    try:
                        from django.conf import settings as dj_settings

                        default_slug = getattr(dj_settings, "DEFAULT_CHANNEL_SLUG", "default-channel")
                        default_currency = os.environ.get("DEFAULT_CURRENCY") or getattr(dj_settings, "DEFAULT_CURRENCY", "USD")
                        default_country = os.environ.get("DEFAULT_COUNTRY", "US")
                        Channel.objects.get_or_create(
                            slug=default_slug,
                            defaults={
                                "name": "Default channel",
                                "is_active": True,
                                "currency_code": default_currency,
                                "default_country": default_country,
                            },
                        )
                    except Exception:
                        pass
            except Exception as e3:
                _log(
                    "smart_migrate.py:ensure_channel",
                    "schema_editor fallback failed",
                    {"error": str(e3), "error_type": type(e3).__name__},
                    "H14",
                )
                ok = False
        print(f"✅ channel_channel exists after migrate: {ok}")
        _log("smart_migrate.py:ensure_channel", "channel_channel after migrate", {"exists": ok}, "H14")
        return ok
    except Exception as e:
        _log(
            "smart_migrate.py:ensure_channel",
            "ensure channel exception",
            {"error": str(e), "error_type": type(e).__name__},
            "H14",
        )
        return False

def fake_problematic_migrations():
    """Mark known problematic migrations as fake"""
    problematic_migrations = [
        ('site', '0014'),  # display_gross_prices duplicate column
        ('site', '0015'),  # track_inventory_by_default duplicate column in site_sitesettings
        ('site', '0017_auto_20180803_0528'),  # site_sitesettingstranslation table already exists (partial migration)
        ('checkout', '0008'),  # cart_cart table rename issue
    ]
    
    for app, migration in problematic_migrations:
        try:
            print(f"🔧 Attempting to fake {app}.{migration}...")
            call_command('migrate', app, migration, fake=True, verbosity=1, interactive=False)
            print(f"✅ Faked {app}.{migration}")
        except Exception as e:
            print(f"⚠️  Could not fake {app}.{migration}: {e}")
    
    # Check if product app migrations are needed for inventory
    # If product migrations haven't run, we may need to fake the dependency
    try:
        from django.db.migrations.recorder import MigrationRecorder
        recorder = MigrationRecorder(connection)
        # Django returns a set of (app, name) tuples here.
        applied_migrations = {}
        for row in recorder.applied_migrations():
            try:
                app, name = row  # tuple form
                applied_migrations[app] = name
            except Exception:
                try:
                    applied_migrations[row.app] = row.name  # model-like fallback
                except Exception:
                    pass
        
        # Check if product migration that inventory depends on exists
        if 'product' not in applied_migrations or '0202_category_product_category_tree_id_lf1e1' not in applied_migrations.get('product', ''):
            print("⚠️  Product migrations may not be complete - inventory migration may fail")
            print("   This is OK - inventory tables will be created when product migrations complete")
    except Exception as e:
        print(f"⚠️  Could not check migration status: {e}")

def migrate_custom_apps():
    """Migrate only our custom apps"""
    # Migrate apps that don't depend on Saleor first
    independent_apps = ['regions', 'currency', 'branches']
    dependent_apps = ['inventory']  # Depends on product app
    
    print("\n" + "=" * 80)
    print("MIGRATING CUSTOM APPS")
    print("=" * 80)
    
    # First, migrate independent apps
    for app in independent_apps:
        try:
            print(f"\n📦 Migrating {app}...")
            call_command('migrate', app, verbosity=2, interactive=False)
            print(f"✅ {app} migrations complete")
        except Exception as e:
            print(f"⚠️  {app} migration error: {e}")
            import traceback
            traceback.print_exc()
    
    # Then try dependent apps
    for app in dependent_apps:
        try:
            print(f"\n📦 Migrating {app} (may depend on Saleor migrations)...")
            call_command('migrate', app, verbosity=2, interactive=False)
            print(f"✅ {app} migrations complete")
        except Exception as e:
            error_str = str(e)
            if 'does not exist' in error_str or 'dependency' in error_str.lower():
                print(f"⚠️  {app} migration skipped - dependencies not met: {e}")
                print(f"   This is OK - {app} tables will be created when dependencies are ready")
            else:
                print(f"⚠️  {app} migration error: {e}")
                import traceback
                traceback.print_exc()

def seed_default_regions():
    """Ensure default Region rows exist (needed for branchCreate FK)."""
    try:
        if not check_table_exists("regions"):
            _log("smart_migrate.py:seed_default_regions", "regions table missing; skipping seed", {}, "H8")
            return
        from saleor_extensions.regions.models import Region
        if Region.objects.exists():
            _log("smart_migrate.py:seed_default_regions", "regions already seeded", {"count": Region.objects.count()}, "H8")
            return
        defaults = [
            # Use explicit PKs to match common UI assumptions (regionId=1 etc.)
            {"id": 1, "code": "INDIA", "name": "India", "default_currency": "INR", "tax_rate": 3, "timezone": "Asia/Kolkata", "locale": "en-IN", "is_active": True},
            {"id": 2, "code": "UK", "name": "United Kingdom", "default_currency": "GBP", "tax_rate": 20, "timezone": "Europe/London", "locale": "en-GB", "is_active": True},
            {"id": 3, "code": "UAE", "name": "United Arab Emirates", "default_currency": "AED", "tax_rate": 5, "timezone": "Asia/Dubai", "locale": "en-AE", "is_active": True},
        ]
        for row in defaults:
            Region.objects.create(**row)
        _log("smart_migrate.py:seed_default_regions", "seeded default regions", {"created": len(defaults)}, "H8")
    except Exception as e:
        _log("smart_migrate.py:seed_default_regions", "failed seeding regions", {"error": str(e), "error_type": type(e).__name__}, "H8")

def _verify_custom_tables():
    checks = [
        ("branches", "branches"),
        ("regions", "regions"),
        ("currency", "currencies"),
        ("currency", "exchange_rates"),
        ("inventory", "branch_inventory"),
        ("inventory", "stock_movements"),
        ("inventory", "stock_transfers"),
        ("inventory", "low_stock_alerts"),
    ]
    missing = []
    for app, table in checks:
        exists = check_table_exists(table)
        status = "✅" if exists else "❌"
        print(f"{status} {app}.{table}: {'exists' if exists else 'missing'}")
        if not exists:
            missing.append(table)
    _log("smart_migrate.py:verify", "verified custom tables", {"missing": missing, "missingCount": len(missing)}, "H7")
    return missing

def _verify_required_saleor_tables():
    # These are core tables Saleor's GraphQL resolvers hit for the admin dashboard.
    # If any are missing, GraphQL can return 400 with "relation ... does not exist".
    required = [
        "channel_channel",
        "product_product",
        "product_productvariant",
        "product_productchannellisting",
        "tax_taxclass",
    ]
    missing = [t for t in required if not check_table_exists(t)]
    _log(
        "smart_migrate.py:verify_saleor",
        "verified required Saleor tables",
        {"missing": missing, "missingCount": len(missing)},
        "H14",
    )
    if missing:
        print(f"❌ Missing required Saleor tables: {missing}")
    else:
        print("✅ Required Saleor tables exist")
    return missing

def ensure_saleor_core_apps():
    """
    Try to migrate the critical Saleor apps needed by the Admin dashboard.
    This is safer than trying to "ALTER TABLE" our way out of missing relations.
    """
    # #region agent log
    _log(
        "smart_migrate.py:ensure_saleor_core_apps:entry",
        "Ensuring critical Saleor apps are migrated",
        {"hypothesisId": "H19"},
        "H19",
    )
    # #endregion
    # NOTE: Saleor has an app named `site` (distinct from Django's `sites`).
    # The `site` migrations are currently the #1 source of "column already exists" failures
    # which block downstream apps (tax/product) from creating required tables.
    apps = ["contenttypes", "auth", "sites", "site", "core", "channel", "tax", "product", "warehouse"]
    results = []

    def _maybe_fix_site_duplicate_column(err: Exception) -> bool:
        """
        Recover from a common partially-migrated DB state:
          column "track_inventory_by_default" of relation "site_sitesettings" already exists
        In that case, faking `site.0015` is safe because the column is already present.
        """
        msg = str(err)
        if "site_sitesettingstranslation" in msg and "already exists" in msg:
            try:
                print("🔧 Detected existing site_sitesettingstranslation table; faking site.0017 and continuing...")
                call_command("migrate", "site", "0017_auto_20180803_0528", verbosity=1, interactive=False, fake=True)
                return True
            except Exception as e:
                print(f"⚠️  Failed to fake site.0017_auto_20180803_0528: {e}")
                return False
        if "site_sitesettings" in msg and "track_inventory_by_default" in msg and "already exists" in msg:
            try:
                print("🔧 Detected duplicate column on site_sitesettings; faking site.0015 and continuing...")
                call_command("migrate", "site", "0015", verbosity=1, interactive=False, fake=True)
                return True
            except Exception as e:
                print(f"⚠️  Failed to fake site.0015: {e}")
                return False
        if "site_sitesettings" in msg and "display_gross_prices" in msg and "already exists" in msg:
            try:
                print("🔧 Detected duplicate column on site_sitesettings; faking site.0014 and continuing...")
                call_command("migrate", "site", "0014", verbosity=1, interactive=False, fake=True)
                return True
            except Exception as e:
                print(f"⚠️  Failed to fake site.0014: {e}")
                return False
        return False

    for app in apps:
        try:
            print(f"📦 Ensuring Saleor app migrated: {app}")
            call_command("migrate", app, verbosity=1, interactive=False)
            results.append({"app": app, "ok": True})
        except Exception as e:
            # Attempt a one-time recovery for known partial-migration conflicts (then retry)
            recovered = _maybe_fix_site_duplicate_column(e)
            if recovered:
                try:
                    print(f"🔁 Retrying migrate for {app} after recovery...")
                    call_command("migrate", app, verbosity=1, interactive=False)
                    results.append({"app": app, "ok": True, "recovered": True})
                    continue
                except Exception as e_retry:
                    e = e_retry
            results.append({"app": app, "ok": False, "error": str(e), "error_type": type(e).__name__})
            print(f"⚠️  Saleor app migrate failed for {app}: {e}")
    _log(
        "smart_migrate.py:ensure_saleor_core_apps:result",
        "Finished ensuring critical Saleor apps",
        {"results": results, "hypothesisId": "H19"},
        "H19",
    )
    return results

def ensure_saleor_productvariant_columns():
    """
    Saleor code expects certain columns on `product_productvariant` but some DBs can be older / partially migrated.
    If missing, add them safely. This fixes runtime failures like:
      - column product_productvariant.sort_order does not exist
      - column product_productvariant.private_metadata does not exist
    """
    try:
        if not check_table_exists("product_productvariant"):
            _log(
                "smart_migrate.py:ensure_productvariant_columns",
                "product_productvariant table missing; skipping sort_order check",
                {},
                "H10",
            )
            return False

        changes = []
        with connection.cursor() as cursor:
            # sort_order
            if not check_column_exists("product_productvariant", "sort_order"):
                cursor.execute(
                    "ALTER TABLE product_productvariant ADD COLUMN IF NOT EXISTS sort_order integer NOT NULL DEFAULT 0;"
                )
                changes.append("sort_order")

            # metadata / private_metadata (Saleor uses JSONField -> jsonb)
            if not check_column_exists("product_productvariant", "metadata"):
                cursor.execute(
                    "ALTER TABLE product_productvariant ADD COLUMN IF NOT EXISTS metadata jsonb NOT NULL DEFAULT '{}'::jsonb;"
                )
                changes.append("metadata")

            if not check_column_exists("product_productvariant", "private_metadata"):
                cursor.execute(
                    "ALTER TABLE product_productvariant ADD COLUMN IF NOT EXISTS private_metadata jsonb NOT NULL DEFAULT '{}'::jsonb;"
                )
                changes.append("private_metadata")

            # external_reference (Saleor uses this for integrations; keep nullable to be safe)
            if not check_column_exists("product_productvariant", "external_reference"):
                cursor.execute(
                    "ALTER TABLE product_productvariant ADD COLUMN IF NOT EXISTS external_reference varchar(250);"
                )
                changes.append("external_reference")

        _log(
            "smart_migrate.py:ensure_productvariant_columns",
            "Ensured product_productvariant columns",
            {"added": changes},
            "H10",
        )
        return True
    except Exception as e:
        _log(
            "smart_migrate.py:ensure_productvariant_columns",
            "Failed ensuring product_productvariant columns",
            {"error": str(e), "error_type": type(e).__name__},
            "H10",
        )
        return False

def ensure_saleor_product_columns():
    """
    Saleor's Product model expects certain columns on `product_product`.
    If the DB is behind, product queries can fail with missing column errors.
    This function adds missing columns that are commonly required.
    """
    # #region agent log
    _log(
        "smart_migrate.py:ensure_product_columns:entry",
        "Starting product_product column repair",
        {"hypothesisId": "H16"},
        "H16",
    )
    # #endregion
    
    try:
        if not check_table_exists("product_product"):
            _log(
                "smart_migrate.py:ensure_product_columns",
                "product_product table missing; skipping",
                {},
                "H15",
            )
            return False

        # #region agent log
        # Check current columns before repair
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT column_name FROM information_schema.columns 
                WHERE table_schema = 'public' 
                AND table_name = 'product_product'
                ORDER BY column_name;
            """)
            existing_columns = [row[0] for row in cursor.fetchall()]
            _log(
                "smart_migrate.py:ensure_product_columns:before",
                "Current product_product columns",
                {"hypothesisId": "H16", "columns": existing_columns, "count": len(existing_columns)},
                "H16",
            )
        # #endregion

        changes = []
        with connection.cursor() as cursor:
            # Metadata columns (commonly missing)
            if not check_column_exists("product_product", "metadata"):
                cursor.execute(
                    "ALTER TABLE product_product ADD COLUMN IF NOT EXISTS metadata jsonb NOT NULL DEFAULT '{}'::jsonb;"
                )
                changes.append("metadata")

            if not check_column_exists("product_product", "private_metadata"):
                cursor.execute(
                    "ALTER TABLE product_product ADD COLUMN IF NOT EXISTS private_metadata jsonb NOT NULL DEFAULT '{}'::jsonb;"
                )
                changes.append("private_metadata")

            if not check_column_exists("product_product", "external_reference"):
                cursor.execute(
                    "ALTER TABLE product_product ADD COLUMN IF NOT EXISTS external_reference varchar(250);"
                )
                changes.append("external_reference")

            # Core product fields (if missing, add with safe defaults)
            if not check_column_exists("product_product", "slug"):
                cursor.execute(
                    "ALTER TABLE product_product ADD COLUMN IF NOT EXISTS slug varchar(255);"
                )
                changes.append("slug")

            if not check_column_exists("product_product", "description_plaintext"):
                cursor.execute(
                    "ALTER TABLE product_product ADD COLUMN IF NOT EXISTS description_plaintext text;"
                )
                changes.append("description_plaintext")

            # Search/document columns (commonly missing in older DBs)
            if not check_column_exists("product_product", "search_document"):
                cursor.execute(
                    "ALTER TABLE product_product ADD COLUMN IF NOT EXISTS search_document tsvector;"
                )
                changes.append("search_document")

        # #region agent log
        _log(
            "smart_migrate.py:ensure_product_columns:after",
            "Product columns repair completed",
            {"hypothesisId": "H16", "added": changes, "addedCount": len(changes)},
            "H16",
        )
        # #endregion

        _log(
            "smart_migrate.py:ensure_product_columns",
            "Ensured product_product columns",
            {"added": changes},
            "H15",
        )
        return True
    except Exception as e:
        _log(
            "smart_migrate.py:ensure_product_columns",
            "Failed ensuring product_product columns",
            {"error": str(e), "error_type": type(e).__name__},
            "H15",
        )
        return False

def main():
    print("=" * 80)
    print("SMART MIGRATION SCRIPT")
    print("=" * 80)
    print()
    
    # Step 1: Check database connection
    try:
        connection.ensure_connection()
        print("✅ Database connection successful")
        _log("smart_migrate.py:db", "database connection successful", {}, "H7")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        _log("smart_migrate.py:db", "database connection failed", {"error": str(e), "error_type": type(e).__name__}, "H7")
        return 1

    # Step 1a: Make post_migrate permission creation resilient so it can't block migrations.
    patch_create_permissions_ignore_duplicates()

    # Step 1b: Ensure Postgres extensions commonly required by Saleor
    ensure_postgres_extensions()
    
    # Step 2: Fix known problematic migrations
    print("\n" + "=" * 80)
    print("FIXING PROBLEMATIC MIGRATIONS")
    print("=" * 80)
    fake_problematic_migrations()
    
    # Step 3: Try to run all migrations
    print("\n" + "=" * 80)
    print("RUNNING ALL MIGRATIONS")
    print("=" * 80)
    
    # #region agent log
    _log(
        "smart_migrate.py:migrate_all:entry",
        "Starting migrate all",
        {"hypothesisId": "H17"},
        "H17",
    )
    # #endregion
    
    try:
        call_command('migrate', verbosity=1, interactive=False)
        print("\n✅ All migrations completed successfully")
        _log("smart_migrate.py:migrate_all", "migrate all completed", {}, "H7")
        
        # #region agent log
        _log(
            "smart_migrate.py:migrate_all:success",
            "All migrations completed successfully",
            {"hypothesisId": "H17"},
            "H17",
        )
        # #endregion
    except Exception as e:
        error_str = str(e)
        print(f"\n⚠️  Migration error: {error_str}")
        _log("smart_migrate.py:migrate_all", "migrate all failed", {"error": error_str, "error_type": type(e).__name__}, "H7")
        
        # #region agent log
        _log(
            "smart_migrate.py:migrate_all:error",
            "Migration error occurred",
            {"hypothesisId": "H17", "error": error_str, "errorType": type(e).__name__},
            "H17",
        )
        # #endregion
        
        # If it's a table/column issue, try to migrate custom apps only
        if 'does not exist' in error_str or 'already exists' in error_str:
            print("\n" + "=" * 80)
            print("FALLBACK: MIGRATING CUSTOM APPS ONLY")
            print("=" * 80)
            
            # #region agent log
            _log(
                "smart_migrate.py:fallback:entry",
                "Starting fallback: custom apps + product migrations",
                {"hypothesisId": "H17"},
                "H17",
            )
            # #endregion
            
            migrate_custom_apps()
            seed_default_regions()
            ensure_saleor_productvariant_columns()
            ensure_saleor_product_columns()
            ensure_saleor_channel_tables()
            # NEW: force critical Saleor apps to migrate so required tables exist
            ensure_saleor_core_apps()
            
            # Try to run product app migrations explicitly
            # #region agent log
            _log(
                "smart_migrate.py:fallback:product_migrate:entry",
                "Attempting explicit product app migrations",
                {"hypothesisId": "H17"},
                "H17",
            )
            # #endregion
            try:
                call_command('migrate', 'product', verbosity=1, interactive=False)
                # #region agent log
                _log(
                    "smart_migrate.py:fallback:product_migrate:success",
                    "Product app migrations completed",
                    {"hypothesisId": "H17"},
                    "H17",
                )
                # #endregion
                print("✅ Product app migrations completed")
            except Exception as e2:
                # #region agent log
                _log(
                    "smart_migrate.py:fallback:product_migrate:error",
                    "Product app migrations failed",
                    {"hypothesisId": "H17", "error": str(e2), "errorType": type(e2).__name__},
                    "H17",
                )
                # #endregion
                print(f"⚠️  Product app migrations failed: {e2}")
                # Continue anyway - column repair should handle missing columns
            
            print("\n" + "=" * 80)
            print("⚠️  Some Saleor migrations failed, but custom app migrations completed")
            print("=" * 80)
            print("\nYou may need to manually fix Saleor migrations later.")
            missing = _verify_custom_tables()
            saleor_missing = _verify_required_saleor_tables()
            return 0 if (not missing and not saleor_missing) else 1
        else:
            return 1
    
    # Step 4: Verify custom app tables exist
    print("\n" + "=" * 80)
    print("VERIFYING CUSTOM APP TABLES")
    print("=" * 80)
    
    seed_default_regions()
    ensure_saleor_productvariant_columns()
    ensure_saleor_product_columns()
    ensure_saleor_channel_tables()
    ensure_saleor_core_apps()
    missing = _verify_custom_tables()
    saleor_missing = _verify_required_saleor_tables()
    if missing:
        print("\n⚠️  Some custom app tables are missing - retrying custom app migrations")
        migrate_custom_apps()
        missing = _verify_custom_tables()
    if not missing:
        print("\n✅ All custom app tables exist!")
    else:
        print("\n❌ Some custom app tables are still missing after retry:", missing)
        return 1
    if saleor_missing:
        print("\n❌ Missing required Saleor tables after migrations:", saleor_missing)
        return 1
    
    print("\n" + "=" * 80)
    print("✅ Migration process complete!")
    print("=" * 80)
    return 0

if __name__ == '__main__':
    sys.exit(main())

