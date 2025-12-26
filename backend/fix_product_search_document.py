#!/usr/bin/env python3
"""
Quick fix script to add missing search columns to product_product table.
These columns are required by Saleor's GraphQL queries but may be missing in some databases.
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

def add_search_columns():
    """Add search_document and search_vector columns to product_product table if they don't exist"""
    try:
        if not check_table_exists("product_product"):
            print("❌ Table product_product does not exist. Run migrations first.")
            return False
        
        changes = []
        
        # Add search_document column (tsvector for full-text search)
        if not check_column_exists("product_product", "search_document"):
            print("🔧 Adding search_document column to product_product table...")
            with connection.cursor() as cursor:
                cursor.execute("""
                    ALTER TABLE product_product 
                    ADD COLUMN IF NOT EXISTS search_document tsvector;
                """)
            changes.append("search_document")
            print("✅ Successfully added search_document column")
        else:
            print("✅ Column search_document already exists")
        
        # Add search_vector column (tsvector for full-text search)
        # Note: Some Saleor versions use search_vector instead of or in addition to search_document
        if not check_column_exists("product_product", "search_vector"):
            print("🔧 Adding search_vector column to product_product table...")
            with connection.cursor() as cursor:
                cursor.execute("""
                    ALTER TABLE product_product 
                    ADD COLUMN IF NOT EXISTS search_vector tsvector;
                """)
            changes.append("search_vector")
            print("✅ Successfully added search_vector column")
        else:
            print("✅ Column search_vector already exists")
        
        if changes:
            print(f"\n✅ Added {len(changes)} column(s): {', '.join(changes)}")
        else:
            print("\n✅ All search columns already exist")
        
        return True
    except Exception as e:
        print(f"❌ Error adding search columns: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("=" * 80)
    print("FIXING MISSING SEARCH COLUMNS (search_document, search_vector)")
    print("=" * 80)
    
    with transaction.atomic():
        success = add_search_columns()
    
    if success:
        print("\n✅ Fix completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Fix failed. Check the error messages above.")
        sys.exit(1)

