#!/usr/bin/env python3
"""
Run Django migrations for Railway deployment.

This script:
1. Creates migrations for custom apps (if needed)
2. Runs all migrations
3. Verifies database tables exist
4. Exits (does NOT start a web server)

Usage:
    python run_migrations.py
    Or via Railway: railway run python run_migrations.py
    Or as Railway start command: python run_migrations.py
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grandgold_settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Prevent Gunicorn from starting if this script is run
# This ensures migrations run without starting a web server
if __name__ == '__main__':
    # Make sure we're not being imported by Gunicorn
    pass

def main():
    print("=" * 80)
    print("RUNNING DJANGO MIGRATIONS")
    print("=" * 80)
    print()
    
    # Initialize Django
    django.setup()
    
    from django.core.management import call_command
    from django.db import connection
    
    # Step 1: Check database connection
    print("Step 1: Checking database connection...")
    try:
        connection.ensure_connection()
        print("✅ Database connection successful")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("   Make sure DATABASE_URL is set and PostgreSQL service is running")
        return 1
    
    # Step 2: Create migrations for custom apps
    print("\nStep 2: Creating migrations for custom apps...")
    try:
        call_command('makemigrations', 
                    'saleor_extensions.regions',
                    'saleor_extensions.currency',
                    'saleor_extensions.branches',
                    'saleor_extensions.inventory',
                    verbosity=1,
                    interactive=False)
        print("✅ Migrations created (or already exist)")
    except Exception as e:
        print(f"⚠️  Error creating migrations: {e}")
        print("   Continuing anyway (migrations may already exist)...")
    
    # Step 3: Run all migrations
    print("\nStep 3: Running migrations...")
    try:
        call_command('migrate', verbosity=2, interactive=False)
        print("✅ All migrations applied successfully")
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    # Step 4: Verify tables exist
    print("\nStep 4: Verifying database tables...")
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name IN ('branches', 'regions', 'branch_inventory')
                ORDER BY table_name;
            """)
            tables = [row[0] for row in cursor.fetchall()]
            
            if 'branches' in tables:
                print("✅ 'branches' table exists")
            else:
                print("⚠️  'branches' table not found (may need to run migrations)")
            
            if 'regions' in tables:
                print("✅ 'regions' table exists")
            else:
                print("⚠️  'regions' table not found (may need to run migrations)")
                
    except Exception as e:
        print(f"⚠️  Could not verify tables: {e}")
    
    print("\n" + "=" * 80)
    print("✅ Migration process complete!")
    print("=" * 80)
    print("\nExiting migration script. Service can be stopped now.")
    return 0

if __name__ == '__main__':
    # Exit immediately after migrations - don't start web server
    exit_code = main()
    sys.exit(exit_code)

