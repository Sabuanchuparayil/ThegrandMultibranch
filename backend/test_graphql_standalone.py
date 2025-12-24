"""
Test GraphQL queries and mutations locally - Standalone Schema
This tests our inventory schema without requiring Saleor integration
"""
import os
import sys
import django
from graphene.test import Client
from graphene import Schema

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'saleor.settings')

try:
    django.setup()
    print("✅ Django setup successful\n")
except Exception as e:
    print(f"❌ Django setup failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Import schema
try:
    from saleor_extensions.inventory.schema import (
        InventoryQueries,
        InventoryMutations,
    )
    print("✅ Successfully imported inventory schema\n")
except Exception as e:
    print(f"❌ Failed to import inventory schema: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Create standalone schema (without Saleor)
schema = Schema(query=InventoryQueries, mutation=InventoryMutations)
client = Client(schema)

print("=" * 70)
print("GraphQL Inventory API Test - Standalone Schema")
print("=" * 70)
print()

# Test 1: Introspection query
print("📋 Test 1: Schema Introspection")
print("-" * 70)

introspection_query = """
{
  __schema {
    queryType {
      name
      fields {
        name
        description
        args {
          name
          type {
            name
          }
        }
      }
    }
    mutationType {
      name
      fields {
        name
        description
        args {
          name
          type {
            name
          }
        }
      }
    }
  }
}
"""

try:
    result = client.execute(introspection_query)
    
    if 'errors' in result:
        print("❌ Errors in introspection:")
        for error in result['errors']:
            print(f"   - {error.get('message', error)}")
            if 'locations' in error:
                for loc in error['locations']:
                    print(f"     Line {loc.get('line')}, Column {loc.get('column')}")
    else:
        print("✅ Introspection successful!")
        
        # Show available queries
        if 'data' in result and result['data'] and '__schema' in result['data']:
            query_type = result['data']['__schema'].get('queryType', {})
            mutation_type = result['data']['__schema'].get('mutationType', {})
            
            if query_type:
                queries = query_type.get('fields', [])
                print(f"\n   ✅ Available Queries ({len(queries)}):")
                for query in queries:
                    name = query.get('name', '')
                    desc = query.get('description', 'No description')
                    print(f"      • {name}")
                    if desc and desc != 'No description':
                        print(f"        {desc}")
            
            if mutation_type:
                mutations = mutation_type.get('fields', [])
                if mutations:
                    print(f"\n   ✅ Available Mutations ({len(mutations)}):")
                    for mutation in mutations:
                        name = mutation.get('name', '')
                        desc = mutation.get('description', 'No description')
                        print(f"      • {name}")
                        if desc and desc != 'No description':
                            print(f"        {desc}")
            
except Exception as e:
    print(f"❌ Introspection failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("Example Queries (require database setup)")
print("=" * 70)
print()

print("""
📝 Example Queries:

1. Get Branch Inventory:
   Query branch inventory with low stock filtering

2. Get Stock Movements:
   Query stock movement history for a branch

3. Adjust Stock:
   Mutation to increase or decrease stock

4. Create Stock Transfer:
   Mutation to create a transfer between branches

5. Process Stock Transfer:
   Mutation to approve/complete a transfer

Note: These queries require:
  - Database setup and migrations
  - Test data (branches, product variants)
  - Proper IDs for branches and products
""")

print("\n" + "=" * 70)
print("✅ Standalone schema test complete!")
print("=" * 70)
print("\n💡 Next steps:")
print("   1. Run migrations: python manage.py migrate")
print("   2. Create test data in Django admin")
print("   3. Test with actual GraphQL client or playground")
print("   4. Integrate with Saleor schema (optional)")

