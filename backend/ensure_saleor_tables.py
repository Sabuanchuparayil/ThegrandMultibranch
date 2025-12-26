#!/usr/bin/env python3
"""
Ensure critical Saleor tables exist in the database.
This script runs BEFORE Django setup to avoid migration issues.

Uses psycopg2 directly to avoid Django boot problems.
"""
import os
import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def get_db_config():
    """Get database configuration from environment"""
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        # Try parsing individual components
        return {
            'host': os.environ.get('DB_HOST', 'localhost'),
            'port': os.environ.get('DB_PORT', '5432'),
            'database': os.environ.get('DB_NAME', 'postgres'),
            'user': os.environ.get('DB_USER', 'postgres'),
            'password': os.environ.get('DB_PASSWORD', ''),
        }
    
    # Parse DATABASE_URL (format: postgresql://user:password@host:port/dbname)
    import urllib.parse
    parsed = urllib.parse.urlparse(database_url)
    return {
        'host': parsed.hostname,
        'port': parsed.port or 5432,
        'database': parsed.path[1:] if parsed.path else 'postgres',
        'user': parsed.username,
        'password': parsed.password,
    }

def check_table_exists(cursor, table_name):
    """Check if a table exists"""
    cursor.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name = %s
        );
    """, [table_name])
    return cursor.fetchone()[0]

def create_productchannellisting_table(cursor):
    """Create product_productchannellisting table if it doesn't exist"""
    if check_table_exists(cursor, 'product_productchannellisting'):
        print("✅ product_productchannellisting already exists")
        return True
    
    print("🔧 Creating product_productchannellisting table...")
    
    # Create the table with essential columns based on Saleor's ProductChannelListing model
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS product_productchannellisting (
            id SERIAL PRIMARY KEY,
            product_id INTEGER NOT NULL,
            channel_id INTEGER NOT NULL,
            currency VARCHAR(3) NOT NULL,
            price_amount NUMERIC(20, 2) NOT NULL,
            cost_price_amount NUMERIC(20, 2),
            is_published BOOLEAN NOT NULL DEFAULT FALSE,
            published_at TIMESTAMP WITH TIME ZONE,
            visible_in_listings BOOLEAN NOT NULL DEFAULT FALSE,
            available_for_purchase_at TIMESTAMP WITH TIME ZONE,
            created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
            updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
            CONSTRAINT product_productchannellisting_product_id_channel_id_key UNIQUE (product_id, channel_id)
        );
    """)
    
    # Create indexes
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS product_productchannellisting_product_id_idx 
        ON product_productchannellisting(product_id);
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS product_productchannellisting_channel_id_idx 
        ON product_productchannellisting(channel_id);
    """)
    
    print("✅ product_productchannellisting table created")
    return True

def ensure_critical_saleor_tables():
    """Ensure all critical Saleor tables exist"""
    print("=" * 80)
    print("ENSURING CRITICAL SALEOR TABLES EXIST")
    print("=" * 80)
    
    try:
        db_config = get_db_config()
        conn = psycopg2.connect(**db_config)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # List of critical tables to check/create
        critical_tables = [
            'product_productchannellisting',
            'product_productvariant',
            'tax_taxclass',
            'channel_channel',
        ]
        
        created = []
        existing = []
        
        # Create product_productchannellisting (most critical for GraphQL queries)
        if create_productchannellisting_table(cursor):
            created.append('product_productchannellisting')
        
        # Check other critical tables
        for table in critical_tables:
            if table == 'product_productchannellisting':
                continue  # Already handled
            
            if check_table_exists(cursor, table):
                existing.append(table)
                print(f"✅ {table} already exists")
            else:
                print(f"⚠️  {table} does not exist (will be created by migrations)")
        
        cursor.close()
        conn.close()
        
        print("\n" + "=" * 80)
        print("SUMMARY")
        print("=" * 80)
        print(f"✅ Created: {created}")
        print(f"✅ Existing: {existing}")
        print("=" * 80)
        
        return len(created) > 0
        
    except Exception as e:
        print(f"❌ Error ensuring Saleor tables: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = ensure_critical_saleor_tables()
    sys.exit(0 if success else 1)

