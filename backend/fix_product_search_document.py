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
    """Add all search-related columns to product_product table if they don't exist.
    
    Saleor requires multiple search columns for full-text search functionality:
    - search_document: tsvector for full-text search indexing
    - search_vector: tsvector for full-text search indexing (alternative/additional)
    - search_index_dirty: boolean flag to track if search index needs rebuilding
    """
    try:
        if not check_table_exists("product_product"):
            print("❌ Table product_product does not exist. Run migrations first.")
            return False
        
        changes = []
        
        # Define all columns that Saleor's GraphQL queries might need
        # This includes search columns, timestamp columns, and foreign key columns
        required_columns = [
            # Search-related columns
            {
                'name': 'search_document',
                'type': 'tsvector',
                'description': 'Full-text search document (tsvector)'
            },
            {
                'name': 'search_vector',
                'type': 'tsvector',
                'description': 'Full-text search vector (tsvector)'
            },
            {
                'name': 'search_index_dirty',
                'type': 'boolean',
                'default': 'DEFAULT false',
                'description': 'Flag to track if search index needs rebuilding'
            },
            # Timestamp columns (Saleor uses these for product queries)
            {
                'name': 'created_at',
                'type': 'timestamp with time zone',
                'default': 'DEFAULT CURRENT_TIMESTAMP',
                'description': 'Product creation timestamp'
            },
            # Foreign key columns (Saleor uses these for product relationships)
            {
                'name': 'default_variant_id',
                'type': 'integer',
                'nullable': True,
                'description': 'Foreign key to default product variant'
            },
        ]
        
        # Add each column if it doesn't exist
        for col in required_columns:
            if not check_column_exists("product_product", col['name']):
                print(f"🔧 Adding {col['name']} column ({col['description']})...")
                with connection.cursor() as cursor:
                    default_clause = col.get('default', '')
                    nullable = 'NULL' if col.get('nullable', False) else 'NOT NULL'
                    
                    if default_clause:
                        cursor.execute(f"""
                            ALTER TABLE product_product 
                            ADD COLUMN IF NOT EXISTS {col['name']} {col['type']} {nullable} {default_clause};
                        """)
                    else:
                        cursor.execute(f"""
                            ALTER TABLE product_product 
                            ADD COLUMN IF NOT EXISTS {col['name']} {col['type']} {nullable};
                        """)
                changes.append(col['name'])
                print(f"✅ Successfully added {col['name']} column")
            else:
                print(f"✅ Column {col['name']} already exists")
        
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
    print("FIXING MISSING PRODUCT COLUMNS")
    print("Adding: search_document, search_vector, search_index_dirty, created_at, default_variant_id")
    print("=" * 80)
    
    with transaction.atomic():
        success = add_search_columns()
    
    if success:
        print("\n✅ Fix completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Fix failed. Check the error messages above.")
        sys.exit(1)

