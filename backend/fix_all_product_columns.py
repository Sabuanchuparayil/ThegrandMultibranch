#!/usr/bin/env python3
"""
Comprehensive fix script to add ALL missing Saleor Product columns to product_product table.
This script adds all columns that Saleor's GraphQL queries and resolvers might need,
preventing 400 errors from missing database columns.

This is a comprehensive solution that adds all commonly required columns at once,
rather than fixing them one by one as errors occur.
"""
import os
import sys
import psycopg2

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grandgold_settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def _connect():
    dsn = os.environ.get("DATABASE_URL")
    if not dsn:
        raise RuntimeError("DATABASE_URL is not set; cannot apply DB repairs.")
    return psycopg2.connect(dsn)

def check_column_exists(table_name, column_name):
    """Check if a column exists in a table"""
    with _connect() as conn, conn.cursor() as cursor:
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
    with _connect() as conn, conn.cursor() as cursor:
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = %s
            );
        """, [table_name])
        return cursor.fetchone()[0]

def add_all_product_columns():
    """Add ALL columns that Saleor's Product model and GraphQL resolvers might need.
    
    This comprehensive list includes:
    - Search-related columns (for full-text search)
    - Timestamp columns (for sorting and filtering)
    - Foreign key columns (for relationships)
    - Rating/review columns (for product ratings)
    - Metadata columns (for extensibility)
    - Other commonly used columns
    """
    try:
        if not check_table_exists("product_product"):
            print("❌ Table product_product does not exist. Run migrations first.")
            return False
        
        changes = []
        
        # Comprehensive list of ALL columns that Saleor might need
        # Organized by category for better maintainability
        all_required_columns = [
            # ============================================================
            # Search-related columns (for full-text search functionality)
            # ============================================================
            {
                'name': 'search_document',
                'type': 'tsvector',
                'nullable': True,
                'description': 'Full-text search document (tsvector)'
            },
            {
                'name': 'search_vector',
                'type': 'tsvector',
                'nullable': True,
                'description': 'Full-text search vector (tsvector)'
            },
            {
                'name': 'search_index_dirty',
                'type': 'boolean',
                'nullable': True,
                'default': 'DEFAULT false',
                'description': 'Flag to track if search index needs rebuilding'
            },
            
            # ============================================================
            # Timestamp columns (for sorting, filtering, and auditing)
            # ============================================================
            {
                'name': 'created_at',
                'type': 'timestamp with time zone',
                'nullable': True,
                'default': 'DEFAULT CURRENT_TIMESTAMP',
                'description': 'Product creation timestamp'
            },
            # Note: updated_at should already exist in Saleor's Product model
            
            # ============================================================
            # Foreign key columns (for relationships)
            # ============================================================
            {
                'name': 'default_variant_id',
                'type': 'integer',
                'nullable': True,
                'description': 'Foreign key to default product variant'
            },
            {
                'name': 'category_id',
                'type': 'integer',
                'nullable': True,
                'description': 'Foreign key to product category (if not already exists)'
            },
            {
                'name': 'tax_class_id',
                'type': 'integer',
                'nullable': True,
                'description': 'Foreign key to tax class (for tax calculation)'
            },
            
            # ============================================================
            # Rating and review columns
            # ============================================================
            {
                'name': 'rating',
                'type': 'numeric(3, 2)',
                'nullable': True,
                'default': 'DEFAULT NULL',
                'description': 'Product rating (0.00 to 5.00)'
            },
            
            # ============================================================
            # Metadata columns (for extensibility)
            # ============================================================
            {
                'name': 'metadata',
                'type': 'jsonb',
                'nullable': True,
                'default': "DEFAULT '{}'::jsonb",
                'description': 'Public metadata (JSON)'
            },
            {
                'name': 'private_metadata',
                'type': 'jsonb',
                'nullable': True,
                'default': "DEFAULT '{}'::jsonb",
                'description': 'Private metadata (JSON)'
            },
            {
                'name': 'external_reference',
                'type': 'varchar(250)',
                'nullable': True,
                'description': 'External reference ID'
            },
            
            # ============================================================
            # Additional product fields
            # ============================================================
            {
                'name': 'price',
                'type': 'numeric(20, 2)',
                'nullable': True,
                'default': 'DEFAULT NULL',
                'description': 'Legacy/compat product price column (some migrations expect this)'
            },
            {
                'name': 'slug',
                'type': 'varchar(255)',
                'nullable': True,
                'description': 'Product slug (URL-friendly identifier)'
            },
            {
                'name': 'description_plaintext',
                'type': 'text',
                'nullable': True,
                'description': 'Plain text description (without HTML)'
            },
            {
                'name': 'weight',
                'type': 'numeric(10, 3)',
                'nullable': True,
                'description': 'Product weight in grams'
            },
            {
                'name': 'charge_taxes',
                'type': 'boolean',
                'nullable': True,
                'default': 'DEFAULT true',
                'description': 'Whether to charge taxes on this product'
            },
        ]
        
        # Add each column if it doesn't exist
        for col in all_required_columns:
            if not check_column_exists("product_product", col['name']):
                print(f"🔧 Adding {col['name']} column ({col['description']})...")
                with _connect() as conn, conn.cursor() as cursor:
                    default_clause = col.get('default', '')
                    nullable = 'NULL' if col.get('nullable', True) else 'NOT NULL'

                    if default_clause:
                        cursor.execute(
                            f"ALTER TABLE product_product "
                            f"ADD COLUMN IF NOT EXISTS {col['name']} {col['type']} {nullable} {default_clause};"
                        )
                    else:
                        cursor.execute(
                            f"ALTER TABLE product_product "
                            f"ADD COLUMN IF NOT EXISTS {col['name']} {col['type']} {nullable};"
                        )
                changes.append(col['name'])
                print(f"✅ Successfully added {col['name']} column")
            else:
                print(f"✅ Column {col['name']} already exists")
        
        if changes:
            print(f"\n✅ Added {len(changes)} column(s): {', '.join(changes)}")
        else:
            print("\n✅ All required columns already exist")
        
        return True
    except Exception as e:
        print(f"❌ Error adding product columns: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("=" * 80)
    print("COMPREHENSIVE PRODUCT COLUMN FIX")
    print("Adding ALL required Saleor Product columns to prevent GraphQL 400 errors")
    print("=" * 80)
    
    # Use direct SQL connection instead of Django transactions to avoid boot failures
    success = add_all_product_columns()
    
    if success:
        print("\n✅ Fix completed successfully!")
        print("All required columns have been added to product_product table.")
        print("GraphQL queries should now work without 400 errors.")
        sys.exit(0)
    else:
        print("\n❌ Fix failed. Check the error messages above.")
        sys.exit(1)

