#!/usr/bin/env python3
"""
Quick fix script to add missing search_document column to product_product table.
This column is required by Saleor's GraphQL queries but may be missing in some databases.
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grandgold_settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

django.setup()

from django.db import connection, transaction

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

def add_search_document_column():
    """Add search_document column to product_product table if it doesn't exist"""
    try:
        if not check_table_exists("product_product"):
            print("❌ Table product_product does not exist. Run migrations first.")
            return False
        
        if check_column_exists("product_product", "search_document"):
            print("✅ Column search_document already exists in product_product table")
            return True
        
        print("🔧 Adding search_document column to product_product table...")
        with connection.cursor() as cursor:
            cursor.execute("""
                ALTER TABLE product_product 
                ADD COLUMN IF NOT EXISTS search_document tsvector;
            """)
        
        print("✅ Successfully added search_document column to product_product table")
        return True
    except Exception as e:
        print(f"❌ Error adding search_document column: {e}")
        return False

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

if __name__ == '__main__':
    print("=" * 80)
    print("FIXING MISSING search_document COLUMN")
    print("=" * 80)
    
    with transaction.atomic():
        success = add_search_document_column()
    
    if success:
        print("\n✅ Fix completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Fix failed. Check the error messages above.")
        sys.exit(1)

