"""
Test GraphQL queries and mutations locally
This script demonstrates how to use the GraphQL API
"""
import os
import sys
import django
from graphene.test import Client
from graphene import Schema

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'saleor.settings.base')

try:
    django.setup()
    print("✅ Django setup successful\n")
except Exception as e:
    print(f"❌ Django setup failed: {e}")
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

# Create test schema
schema = Schema(query=InventoryQueries, mutation=InventoryMutations)
client = Client(schema)

print("=" * 70)
print("GraphQL API Test Suite")
print("=" * 70)
print()

# Test 1: Introspection query
print("📋 Test 1: Schema Introspection")
print("-" * 70)

introspection_query = """
{
  __schema {
    queryType {
      fields {
        name
        description
      }
    }
    mutationType {
      fields {
        name
        description
      }
    }
  }
}
"""

try:
    result = client.execute(introspection_query)
    
    if 'errors' in result:
        print("⚠️  Errors in introspection:")
        for error in result['errors']:
            print(f"   - {error}")
    else:
        print("✅ Introspection successful!")
        
        # Show available queries
        if 'data' in result and result['data'] and '__schema' in result['data']:
            query_type = result['data']['__schema'].get('queryType', {})
            mutation_type = result['data']['__schema'].get('mutationType', {})
            
            queries = query_type.get('fields', [])
            mutations = mutation_type.get('fields', [])
            
            print(f"\n   Available Queries ({len(queries)}):")
            for query in queries[:10]:  # Show first 10
                print(f"      - {query['name']}: {query.get('description', 'No description')}")
            
            if mutations:
                print(f"\n   Available Mutations ({len(mutations)}):")
                for mutation in mutations[:10]:  # Show first 10
                    print(f"      - {mutation['name']}: {mutation.get('description', 'No description')}")
            
except Exception as e:
    print(f"❌ Introspection failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("Example Queries")
print("=" * 70)
print()

# Example queries (commented out - require actual data)
print("""
📝 Example Queries (require database setup):

1. Get Branch Inventory:
```graphql
query {
  branchInventory(branchId: "1", lowStockOnly: false) {
    id
    quantity
    availableQuantity
    isLowStock
    branch {
      name
      code
    }
    productVariant {
      id
      name
      sku
    }
  }
}
```

2. Get Stock Movements:
```graphql
query {
  stockMovements(branchId: "1", limit: 10) {
    id
    movementType
    quantity
    referenceNumber
    createdAt
    productVariant {
      name
      sku
    }
  }
}
```

3. Adjust Stock:
```graphql
mutation {
  stockAdjustment(input: {
    branchId: "1"
    productVariantId: "123"
    quantity: 50
    movementType: "IN"
    notes: "Received from supplier"
  }) {
    inventoryItem {
      id
      quantity
      availableQuantity
    }
    stockMovement {
      id
      movementType
      quantity
    }
    errors {
      field
      message
    }
  }
}
```

4. Create Stock Transfer:
```graphql
mutation {
  stockTransferCreate(input: {
    fromBranchId: "1"
    toBranchId: "2"
    productVariantId: "123"
    quantity: 20
    notes: "Transfer to London branch"
  }) {
    stockTransfer {
      id
      transferNumber
      status
      quantity
    }
    errors {
      field
      message
    }
  }
}
```
""")

print("\n" + "=" * 70)
print("✅ Test script complete!")
print("=" * 70)
print("\n💡 Tips:")
print("   1. Run migrations first: python manage.py migrate")
print("   2. Create test data in Django admin")
print("   3. Use GraphQL playground at /graphql/ endpoint")
print("   4. Test queries with actual branch and product variant IDs")

