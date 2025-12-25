#!/usr/bin/env python3
"""
Test script to verify migrations can run.
This helps diagnose migration issues.
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grandgold_settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    print("=" * 80)
    print("TESTING MIGRATIONS")
    print("=" * 80)
    print()
    
    # Check DATABASE_URL
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        print(f"✅ DATABASE_URL is set: ...@{database_url.split('@')[1] if '@' in database_url else 'set'}")
    else:
        print("❌ DATABASE_URL is not set")
        print("   Migrations cannot run without DATABASE_URL")
        return 1
    
    # Initialize Django
    try:
        django.setup()
        print("✅ Django setup successful")
    except Exception as e:
        print(f"❌ Django setup failed: {e}")
        return 1
    
    # Check database connection
    from django.db import connection
    try:
        connection.ensure_connection()
        print("✅ Database connection successful")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return 1
    
    # Check if apps are registered
    from django.apps import apps
    apps_to_check = ['regions', 'currency', 'branches', 'inventory']
    print("\nChecking app registration:")
    for app_label in apps_to_check:
        try:
            app_config = apps.get_app_config(app_label)
            print(f"  ✅ {app_label}: {app_config.name}")
        except Exception as e:
            print(f"  ❌ {app_label}: {e}")
    
    # Try to create migrations
    print("\nTesting makemigrations:")
    from django.core.management import call_command
    from io import StringIO
    
    try:
        output = StringIO()
        call_command('makemigrations', 'regions', 'currency', 'branches', 'inventory', 
                    verbosity=1, interactive=False, stdout=output)
        result = output.getvalue()
        if result:
            print(f"  Output: {result[:500]}")
        else:
            print("  ✅ No new migrations needed (migrations already exist)")
    except Exception as e:
        print(f"  ⚠️  makemigrations error: {e}")
    
    # Try to run migrations
    print("\nTesting migrate:")
    try:
        output = StringIO()
        call_command('migrate', verbosity=1, interactive=False, stdout=output)
        result = output.getvalue()
        if 'No migrations to apply' in result:
            print("  ✅ No migrations to apply (all migrations already applied)")
        elif 'Applying' in result:
            print(f"  ✅ Migrations applied: {result[:500]}")
        else:
            print(f"  Output: {result[:500]}")
    except Exception as e:
        print(f"  ❌ migrate error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    print("\n" + "=" * 80)
    print("✅ Migration test complete!")
    print("=" * 80)
    return 0

if __name__ == '__main__':
    sys.exit(main())

