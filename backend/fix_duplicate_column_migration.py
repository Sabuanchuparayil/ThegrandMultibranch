#!/usr/bin/env python3
"""
Script to fix duplicate column migration issues.
This marks problematic migrations as already applied (fakes them).
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grandgold_settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

django.setup()

from django.core.management import call_command
from django.db import connection

def main():
    print("=" * 80)
    print("FIXING DUPLICATE COLUMN MIGRATION ISSUE")
    print("=" * 80)
    print()
    
    # Check if the column already exists
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='site_sitesettings' 
            AND column_name='display_gross_prices';
        """)
        column_exists = cursor.fetchone() is not None
    
    if column_exists:
        print("✅ Column 'display_gross_prices' already exists in 'site_sitesettings'")
        print("   This means migration site.0014_handle_taxes was partially applied")
        print()
        print("🔧 Marking migration as already applied (fake)...")
        try:
            call_command('migrate', 'site', '0014', '--fake', verbosity=2)
            print("✅ Migration site.0014_handle_taxes marked as applied")
        except Exception as e:
            print(f"⚠️  Error faking migration: {e}")
            print("   You may need to run this manually:")
            print("   python manage.py migrate site 0014 --fake")
    else:
        print("ℹ️  Column 'display_gross_prices' does not exist")
        print("   Migration should run normally")
    
    print()
    print("🔄 Now running all migrations...")
    try:
        call_command('migrate', verbosity=2, interactive=False)
        print("✅ All migrations completed successfully")
    except Exception as e:
        print(f"⚠️  Migration error: {e}")
        print("   Some migrations may have already been applied")
        return 1
    
    print()
    print("=" * 80)
    print("✅ Migration fix complete!")
    print("=" * 80)
    return 0

if __name__ == '__main__':
    sys.exit(main())

