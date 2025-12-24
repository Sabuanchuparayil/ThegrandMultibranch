#!/usr/bin/env python3
"""
Verify database connection and run migrations for Railway deployment.

This script:
1. Checks if DATABASE_URL is set
2. Tests database connection
3. Shows current migration status
4. Runs migrations if needed

Usage:
    python verify_and_migrate.py
    Or via Railway: railway run python verify_and_migrate.py
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grandgold_settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_database_url():
    """Check if DATABASE_URL is set"""
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        # Mask password in output
        masked_url = database_url.split('@')[1] if '@' in database_url else database_url
        print(f"✅ DATABASE_URL is set: ...@{masked_url}")
        return True
    else:
        print("❌ DATABASE_URL is not set")
        print("   Make sure PostgreSQL service is added and connected in Railway")
        return False

def test_database_connection():
    """Test if we can connect to the database"""
    try:
        django.setup()
        from django.db import connection
        connection.ensure_connection()
        print("✅ Database connection successful")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def show_migration_status():
    """Show which migrations need to be applied"""
    try:
        django.setup()
        from django.core.management import call_command
        from io import StringIO
        
        print("\n📋 Checking migration status...")
        output = StringIO()
        call_command('showmigrations', '--plan', stdout=output, no_color=True)
        output.seek(0)
        lines = output.readlines()
        
        unapplied = [line for line in lines if '[ ]' in line]
        if unapplied:
            print(f"⚠️  Found {len(unapplied)} unapplied migrations:")
            for line in unapplied[:10]:  # Show first 10
                print(f"   {line.strip()}")
            if len(unapplied) > 10:
                print(f"   ... and {len(unapplied) - 10} more")
            return False
        else:
            print("✅ All migrations are applied")
            return True
    except Exception as e:
        print(f"❌ Error checking migrations: {e}")
        return False

def run_migrations():
    """Run pending migrations"""
    try:
        django.setup()
        from django.core.management import call_command
        
        print("\n🔄 Running migrations...")
        call_command('migrate', verbosity=2, interactive=False)
        print("✅ Migrations completed successfully")
        return True
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("=" * 80)
    print("DATABASE VERIFICATION AND MIGRATION SCRIPT")
    print("=" * 80)
    print()
    
    # Step 1: Check DATABASE_URL
    if not check_database_url():
        print("\n❌ Cannot proceed without DATABASE_URL")
        print("   Please add PostgreSQL service in Railway and ensure it's connected")
        return 1
    
    # Step 2: Test connection
    if not test_database_connection():
        print("\n❌ Cannot connect to database")
        print("   Check Railway logs for database connection errors")
        return 1
    
    # Step 3: Check migration status
    needs_migrations = not show_migration_status()
    
    # Step 4: Run migrations if needed
    if needs_migrations:
        print("\n" + "=" * 80)
        response = input("Run migrations now? (y/n): ").strip().lower()
        if response == 'y':
            if run_migrations():
                print("\n✅ All done! Your database is ready.")
                return 0
            else:
                return 1
        else:
            print("Skipping migrations. Run manually with: python manage.py migrate")
            return 0
    else:
        print("\n✅ Database is up to date!")
        return 0

if __name__ == '__main__':
    sys.exit(main())

