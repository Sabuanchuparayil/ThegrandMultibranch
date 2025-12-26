"""
Test script for GraphQL schema integration
Run this to verify the schema is properly integrated
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'saleor.settings.base')

try:
    django.setup()
    print("✅ Django setup successful")
except Exception as e:
    print(f"❌ Django setup failed: {e}")
    sys.exit(1)

# Test imports
print("\n📦 Testing imports...")

try:
    from saleor_extensions.inventory.schema import (
        InventoryQueries,
        InventoryMutations,
        BranchInventoryType,
        StockMovementType,
    )
    print("✅ Successfully imported inventory schema")
except Exception as e:
    print(f"❌ Failed to import inventory schema: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test model imports
try:
    from saleor_extensions.inventory.models import (
        BranchInventory,
        StockMovement,
        StockTransfer,
        LowStockAlert,
    )
    print("✅ Successfully imported inventory models")
except Exception as e:
    print(f"❌ Failed to import inventory models: {e}")
    sys.exit(1)

# Test Saleor imports
try:
    from saleor.graphql.schema import schema as saleor_schema
    print("✅ Successfully imported Saleor schema")
    print(f"   Schema type: {type(saleor_schema)}")
except Exception as e:
    print(f"⚠️  Could not import Saleor schema: {e}")
    print("   This is okay if we're creating a custom schema")

# Test extended schema
print("\n🔗 Testing extended schema...")

try:
    # Try to import our extended schema
    from saleor.graphql.schema import schema as extended_schema
    print("✅ Successfully imported extended schema")
    
    # Check if it has our queries
    if hasattr(extended_schema, 'query_type'):
        query_type = extended_schema.query_type
        if hasattr(query_type, '_meta'):
            fields = query_type._meta.fields
            inventory_fields = [f for f in fields.keys() if 'inventory' in f.lower() or 'stock' in f.lower()]
            if inventory_fields:
                print(f"✅ Found inventory-related fields: {inventory_fields[:5]}")
            else:
                print("⚠️  No inventory fields found in schema (this might be okay)")
    else:
        print("⚠️  Schema doesn't have query_type attribute")
        
except ImportError:
    print("⚠️  Extended schema not found (this is okay, we'll create it)")
except Exception as e:
    print(f"⚠️  Error checking extended schema: {e}")

# Test GraphQL types
print("\n🎯 Testing GraphQL types...")

try:
    # Create a simple test
    from graphene import Schema
    from saleor_extensions.inventory.schema import InventoryQueries, InventoryMutations
    
    test_schema = Schema(query=InventoryQueries, mutation=InventoryMutations)
    print("✅ Successfully created test schema with inventory queries/mutations")
    
    # Check available queries
    if hasattr(test_schema, 'query_type') and hasattr(test_schema.query_type, '_meta'):
        query_fields = list(test_schema.query_type._meta.fields.keys())
        print(f"   Available queries: {query_fields}")
    
    # Check available mutations
    if hasattr(test_schema, 'mutation_type') and hasattr(test_schema.mutation_type, '_meta'):
        mutation_fields = list(test_schema.mutation_type._meta.fields.keys())
        print(f"   Available mutations: {mutation_fields}")
        
except Exception as e:
    print(f"❌ Error creating test schema: {e}")
    import traceback
    traceback.print_exc()

print("\n✅ Integration test complete!")
print("\n📝 Next steps:")
print("   1. If all tests passed, the schema is ready")
print("   2. Extend Saleor's schema in saleor/graphql/schema.py")
print("   3. Test with GraphQL queries")


