#!/usr/bin/env python3
"""
Smart migration script that handles problematic migrations gracefully.
Skips migrations that fail due to missing tables/columns and continues with others.
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grandgold_settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

django.setup()

import json
import time

from django.core.management import call_command
from django.db import connection, transaction
from django.db.utils import OperationalError, ProgrammingError

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

def fake_problematic_migrations():
    """Mark known problematic migrations as fake"""
    problematic_migrations = [
        ('site', '0014'),  # display_gross_prices duplicate column
        ('checkout', '0008'),  # cart_cart table rename issue
    ]
    
    for app, migration in problematic_migrations:
        try:
            print(f"🔧 Attempting to fake {app}.{migration}...")
            call_command('migrate', app, migration, '--fake', verbosity=1)
            print(f"✅ Faked {app}.{migration}")
        except Exception as e:
            print(f"⚠️  Could not fake {app}.{migration}: {e}")
    
    # Check if product app migrations are needed for inventory
    # If product migrations haven't run, we may need to fake the dependency
    try:
        from django.db.migrations.recorder import MigrationRecorder
        recorder = MigrationRecorder(connection)
        applied_migrations = {m.app: m.name for m in recorder.applied_migrations()}
        
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

def ensure_saleor_sort_order_column():
    """
    Saleor code expects `product_productvariant.sort_order` but some DBs can be older / partially migrated.
    If missing, add it safely. This fixes runtime failures like:
      column product_productvariant.sort_order does not exist
    """
    try:
        if not check_table_exists("product_productvariant"):
            _log(
                "smart_migrate.py:ensure_sort_order",
                "product_productvariant table missing; skipping sort_order check",
                {},
                "H10",
            )
            return False
        exists = check_column_exists("product_productvariant", "sort_order")
        if exists:
            _log(
                "smart_migrate.py:ensure_sort_order",
                "sort_order column already exists",
                {},
                "H10",
            )
            return True
        with connection.cursor() as cursor:
            cursor.execute(
                "ALTER TABLE product_productvariant ADD COLUMN IF NOT EXISTS sort_order integer NOT NULL DEFAULT 0;"
            )
        _log(
            "smart_migrate.py:ensure_sort_order",
            "Added missing sort_order column to product_productvariant",
            {},
            "H10",
        )
        return True
    except Exception as e:
        _log(
            "smart_migrate.py:ensure_sort_order",
            "Failed to add sort_order column",
            {"error": str(e), "error_type": type(e).__name__},
            "H10",
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
    
    # Step 2: Fix known problematic migrations
    print("\n" + "=" * 80)
    print("FIXING PROBLEMATIC MIGRATIONS")
    print("=" * 80)
    fake_problematic_migrations()
    
    # Step 3: Try to run all migrations
    print("\n" + "=" * 80)
    print("RUNNING ALL MIGRATIONS")
    print("=" * 80)
    try:
        call_command('migrate', verbosity=2, interactive=False)
        print("\n✅ All migrations completed successfully")
        _log("smart_migrate.py:migrate_all", "migrate all completed", {}, "H7")
    except Exception as e:
        error_str = str(e)
        print(f"\n⚠️  Migration error: {error_str}")
        _log("smart_migrate.py:migrate_all", "migrate all failed", {"error": error_str, "error_type": type(e).__name__}, "H7")
        
        # If it's a table/column issue, try to migrate custom apps only
        if 'does not exist' in error_str or 'already exists' in error_str:
            print("\n" + "=" * 80)
            print("FALLBACK: MIGRATING CUSTOM APPS ONLY")
            print("=" * 80)
            migrate_custom_apps()
            seed_default_regions()
            ensure_saleor_sort_order_column()
            
            print("\n" + "=" * 80)
            print("⚠️  Some Saleor migrations failed, but custom app migrations completed")
            print("=" * 80)
            print("\nYou may need to manually fix Saleor migrations later.")
            missing = _verify_custom_tables()
            return 0 if not missing else 1
        else:
            return 1
    
    # Step 4: Verify custom app tables exist
    print("\n" + "=" * 80)
    print("VERIFYING CUSTOM APP TABLES")
    print("=" * 80)
    
    seed_default_regions()
    ensure_saleor_sort_order_column()
    missing = _verify_custom_tables()
    if missing:
        print("\n⚠️  Some custom app tables are missing - retrying custom app migrations")
        migrate_custom_apps()
        missing = _verify_custom_tables()
    if not missing:
        print("\n✅ All custom app tables exist!")
    else:
        print("\n❌ Some custom app tables are still missing after retry:", missing)
        return 1
    
    print("\n" + "=" * 80)
    print("✅ Migration process complete!")
    print("=" * 80)
    return 0

if __name__ == '__main__':
    sys.exit(main())

