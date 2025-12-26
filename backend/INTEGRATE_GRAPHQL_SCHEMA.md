# Integrating GraphQL Schema with Saleor

## Overview

To integrate the inventory GraphQL schema with Saleor, you need to extend Saleor's GraphQL schema.

## Method 1: Extend Saleor's Schema (Recommended)

Create a file to extend Saleor's schema:

**File**: `backend/saleor/graphql/schema.py`

```python
import graphene
from saleor.graphql.schema import Query as SaleorQuery, Mutation as SaleorMutation

# Import your custom queries and mutations
from saleor_extensions.inventory.schema import InventoryQueries, InventoryMutations
from saleor_extensions.branches.schema import BranchQueries, BranchMutations  # If exists

# Extend Saleor's Query
class Query(SaleorQuery, InventoryQueries, graphene.ObjectType):
    pass

# Extend Saleor's Mutation
class Mutation(SaleorMutation, InventoryMutations, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
```

## Method 2: Plugin System (Alternative)

Saleor 3.x supports plugins. You can create a plugin that extends the schema:

**File**: `backend/saleor_extensions/plugins.py`

```python
from saleor.plugins.base_plugin import BasePlugin, ConfigurationTypeField
from saleor.graphql.schema import Query, Mutation
import graphene
from saleor_extensions.inventory.schema import InventoryQueries, InventoryMutations

class InventoryPlugin(BasePlugin):
    PLUGIN_NAME = "Inventory Management"
    PLUGIN_ID = "inventory"
    
    def extend_graphql_schema(self, schema):
        # This would need to be implemented based on Saleor's plugin API
        pass
```

## Method 3: Direct Schema Extension (For Custom Deployment)

If you're deploying separately from Saleor core, you can directly modify the schema:

**File**: `backend/saleor/graphql/schema.py` (create if doesn't exist)

```python
import graphene
from saleor.graphql import schema as saleor_schema

# Import your extensions
from saleor_extensions.inventory.schema import (
    InventoryQueries,
    InventoryMutations,
    BranchInventoryType,
    StockMovementType,
    StockTransferType,
    LowStockAlertType,
)

# Extend the query
class Query(saleor_schema.Query, InventoryQueries, graphene.ObjectType):
    pass

# Extend the mutation  
class Mutation(saleor_schema.Mutation, InventoryMutations, graphene.ObjectType):
    pass

# Create new schema
schema = graphene.Schema(query=Query, mutation=Mutation)
```

## Update URLs (if needed)

If you need to override the GraphQL endpoint:

**File**: `backend/saleor/urls.py` (or create)

```python
from django.urls import path
from saleor.graphql.views import GraphQLView
from saleor.graphql.schema import schema  # Your extended schema

urlpatterns = [
    path('graphql/', GraphQLView.as_view(schema=schema)),
    # ... other URLs
]
```

## Testing the Schema

Once integrated, test with GraphQL queries:

```graphql
# Query branch inventory
query {
  branchInventory(branchId: "1", lowStockOnly: false) {
    id
    quantity
    availableQuantity
    isLowStock
    branch {
      name
    }
    productVariant {
      name
    }
  }
}

# Adjust stock
mutation {
  stockAdjustment(input: {
    branchId: "1"
    productVariantId: "123"
    quantity: 10
    movementType: "IN"
    notes: "Restocked from supplier"
  }) {
    inventoryItem {
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

## Notes

- Ensure all ForeignKey relationships are properly set up
- Test all queries and mutations before production deployment
- Consider adding permissions/authentication checks
- Add proper error handling and validation


