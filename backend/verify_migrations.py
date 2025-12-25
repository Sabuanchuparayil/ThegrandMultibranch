#!/usr/bin/env python3
"""
Quick script to verify that migrations were successful and tables exist.
Run this to check if branches and other custom app tables are created.
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grandgold_settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

django.setup()

from django.db import connection

def check_table_exists(table_name):
    """Check if a table exists"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = %s
            );
        """, [table_name])
        return cursor.fetchone()[0]

def main():
    print("=" * 80)
    print("VERIFYING MIGRATION SUCCESS")
    print("=" * 80)
    print()
    
    # Check database connection
    try:
        connection.ensure_connection()
        print("✅ Database connection successful")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return 1
    
    # Check custom app tables
    print("\n📋 Checking custom app tables:")
    print("-" * 80)
    
    tables_to_check = {
        'branches': 'branches',
        'regions': 'regions',
        'currency': 'currencies',
        'currency': 'exchange_rates',
        'inventory': 'branch_inventory',
        'inventory': 'stock_movements',
        'inventory': 'stock_transfers',
    }
    
    all_exist = True
    for app, table in tables_to_check.items():
        exists = check_table_exists(table)
        status = "✅" if exists else "❌"
        print(f"{status} {table}: {'EXISTS' if exists else 'MISSING'}")
        if not exists:
            all_exist = False
    
    print()
    if all_exist:
        print("=" * 80)
        print("✅ ALL CUSTOM APP TABLES EXIST!")
        print("=" * 80)
        print("\n🎉 Migrations were successful!")
        print("   You can now test GraphQL queries for branches.")
        return 0
    else:
        print("=" * 80)
        print("⚠️  SOME TABLES ARE MISSING")
        print("=" * 80)
        print("\n   You may need to run migrations again:")
        print("   python manage.py migrate")
        return 1

if __name__ == '__main__':
    sys.exit(main())

