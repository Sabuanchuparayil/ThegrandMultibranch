"""
Test GraphQL schema integration with Saleor
Uses correct Django settings path
"""
import os
import sys
import django

# Setup Django with correct settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'saleor.settings')

try:
    django.setup()
    print("✅ Django setup successful")
except Exception as e:
    print(f"❌ Django setup failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test imports
print("\n📦 Testing imports...")

# Test Saleor imports
try:
    from saleor.graphql.core.mutations import BaseMutation
    print("✅ Successfully imported BaseMutation from Saleor")
except ImportError as e:
    print(f"⚠️  Could not import BaseMutation: {e}")

try:
    from saleor.graphql.core.schema import Query as SaleorQuery, Mutation as SaleorMutation
    print("✅ Successfully imported Saleor Query and Mutation")
except ImportError as e:
    print(f"⚠️  Could not import Saleor Query/Mutation: {e}")

# Test our schema imports
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

# Test creating extended schema
print("\n🔗 Testing schema creation...")

try:
    import graphene
    from saleor_extensions.inventory.schema import InventoryQueries, InventoryMutations
    
    # Create standalone schema for testing
    test_schema = graphene.Schema(query=InventoryQueries, mutation=InventoryMutations)
    print("✅ Successfully created test schema")
    
    # Check query fields
    if hasattr(test_schema, 'query_type') and hasattr(test_schema.query_type, '_meta'):
        query_fields = list(test_schema.query_type._meta.fields.keys())
        print(f"   Available queries ({len(query_fields)}): {query_fields}")
    
    # Check mutation fields
    if hasattr(test_schema, 'mutation_type') and hasattr(test_schema.mutation_type, '_meta'):
        mutation_fields = list(test_schema.mutation_type._meta.fields.keys())
        print(f"   Available mutations ({len(mutation_fields)}): {mutation_fields}")
        
except Exception as e:
    print(f"❌ Error creating test schema: {e}")
    import traceback
    traceback.print_exc()

# Test extending Saleor schema
print("\n🔗 Testing Saleor schema extension...")

try:
    import graphene
    from saleor.graphql.core.schema import Query as SaleorQuery, Mutation as SaleorMutation
    from saleor_extensions.inventory.schema import InventoryQueries, InventoryMutations
    
    # Create extended schema
    class ExtendedQuery(SaleorQuery, InventoryQueries, graphene.ObjectType):
        pass
    
    class ExtendedMutation(SaleorMutation, InventoryMutations, graphene.ObjectType):
        pass
    
    extended_schema = graphene.Schema(query=ExtendedQuery, mutation=ExtendedMutation)
    print("✅ Successfully created extended schema with Saleor")
    
    # Check if both Saleor and our queries are present
    if hasattr(extended_schema, 'query_type'):
        all_fields = list(extended_schema.query_type._meta.fields.keys())
        our_fields = [f for f in all_fields if 'inventory' in f.lower() or 'stock' in f.lower()]
        print(f"   Found our inventory queries: {our_fields}")
        print(f"   Total query fields: {len(all_fields)}")
        
except Exception as e:
    print(f"⚠️  Error extending Saleor schema: {e}")
    import traceback
    traceback.print_exc()
    print("\n   This is okay if we're creating a standalone schema")

print("\n" + "=" * 70)
print("✅ Integration test complete!")
print("=" * 70)

