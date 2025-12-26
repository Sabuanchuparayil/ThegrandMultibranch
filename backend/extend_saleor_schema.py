"""
Script to check Saleor schema structure and test integration
Run this to understand how to extend Saleor's schema
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from saleor.graphql import schema as saleor_schema
    print("✅ Successfully imported Saleor schema")
    print(f"Schema module: {saleor_schema.__file__}")
    
    # Check what's in the schema
    print("\n📋 Schema contents:")
    for attr in dir(saleor_schema):
        if not attr.startswith('_'):
            obj = getattr(saleor_schema, attr)
            print(f"  - {attr}: {type(obj).__name__}")
    
    # Check if Query and Mutation exist
    if hasattr(saleor_schema, 'Query'):
        print("\n✅ Query class found")
        query = saleor_schema.Query
        print(f"   Query fields: {[f for f in dir(query) if not f.startswith('_')][:10]}")
    
    if hasattr(saleor_schema, 'Mutation'):
        print("\n✅ Mutation class found")
        mutation = saleor_schema.Mutation
        print(f"   Mutation fields: {[f for f in dir(mutation) if not f.startswith('_')][:10]}")
    
    if hasattr(saleor_schema, 'schema'):
        print("\n✅ Schema object found")
        print(f"   Schema type: {type(saleor_schema.schema)}")
    
except ImportError as e:
    print(f"❌ Error importing Saleor schema: {e}")
    print("\nTrying alternative import...")
    try:
        import saleor.graphql.schema as saleor_schema
        print("✅ Alternative import successful")
    except Exception as e2:
        print(f"❌ Alternative import also failed: {e2}")


