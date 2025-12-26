#!/usr/bin/env python3
"""
Complete reset and reseed script:
1. Clear all mock data
2. Ensure migrations are complete
3. Reseed initial data

Usage:
    python manage.py shell
    >>> exec(open('reset_and_reseed.py').read())
    
Or run directly:
    python reset_and_reseed.py
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grandgold_settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

django.setup()

from django.core.management import call_command
from django.db import connection

# Import scripts
from clear_mock_data import clear_all_mock_data
from create_initial_data import run as seed_initial_data

def ensure_migrations_complete():
    """Ensure all migrations are applied"""
    print("\n" + "=" * 80)
    print("ENSURING MIGRATIONS ARE COMPLETE")
    print("=" * 80)
    
    try:
        # Run migrations for all apps
        print("\n📦 Running migrations...")
        call_command('migrate', verbosity=1, interactive=False)
        print("✅ Migrations complete")
        return True
    except Exception as e:
        print(f"⚠️  Migration error: {e}")
        print("   Attempting to continue anyway...")
        return False

def reset_and_reseed():
    """Complete reset: clear data, migrate, reseed"""
    print("=" * 80)
    print("COMPLETE RESET AND RESEED")
    print("=" * 80)
    
    # Step 1: Clear all mock data
    print("\n" + "=" * 80)
    print("STEP 1: CLEARING MOCK DATA")
    print("=" * 80)
    clear_all_mock_data()
    
    # Step 2: Ensure migrations are complete
    print("\n" + "=" * 80)
    print("STEP 2: ENSURING MIGRATIONS ARE COMPLETE")
    print("=" * 80)
    migrations_ok = ensure_migrations_complete()
    
    if not migrations_ok:
        print("\n⚠️  WARNING: Some migrations may have failed.")
        print("   Proceeding with data seeding anyway...")
        response = input("\nContinue with seeding? (y/n): ")
        if response.lower() != 'y':
            print("Aborted.")
            return
    
    # Step 3: Reseed initial data
    print("\n" + "=" * 80)
    print("STEP 3: RESEEDING INITIAL DATA")
    print("=" * 80)
    seed_initial_data()
    
    print("\n" + "=" * 80)
    print("✅ RESET AND RESEED COMPLETE")
    print("=" * 80)

if __name__ == '__main__':
    reset_and_reseed()

