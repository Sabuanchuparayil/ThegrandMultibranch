"""
Extended GraphQL Schema for Grand Gold & Diamonds
Extends Saleor's default schema with custom queries and mutations

To use this, you need to configure your GraphQL endpoint to use this schema
instead of Saleor's default schema.
"""
import graphene

# Import Saleor's core schema components
try:
    from saleor.graphql.core.schema import Query as SaleorQuery, Mutation as SaleorMutation
    from saleor.graphql import schema as saleor_schema_module
    _SALEOR_AVAILABLE = True
except ImportError:
    print("Warning: Saleor schema not available, using standalone schema")
    _SALEOR_AVAILABLE = False
    SaleorQuery = graphene.ObjectType
    SaleorMutation = graphene.ObjectType

# Import custom extensions
from saleor_extensions.inventory.schema import (
    InventoryQueries,
    InventoryMutations,
)

# Import dashboard/reports queries
try:
    from saleor_extensions.reports.schema import DashboardQueries
    _DASHBOARD_AVAILABLE = True
except ImportError:
    _DASHBOARD_AVAILABLE = False
    DashboardQueries = graphene.ObjectType


# Extend Query with custom queries
if _SALEOR_AVAILABLE:
    if _DASHBOARD_AVAILABLE:
        class Query(SaleorQuery, InventoryQueries, DashboardQueries, graphene.ObjectType):
            """Extended Query class combining Saleor, inventory, and dashboard queries"""
            pass
    else:
        class Query(SaleorQuery, InventoryQueries, graphene.ObjectType):
            """Extended Query class combining Saleor and inventory queries"""
            pass
    
    # Extend Mutation with custom mutations
    class Mutation(SaleorMutation, InventoryMutations, graphene.ObjectType):
        """Extended Mutation class combining Saleor and custom mutations"""
        pass
else:
    # Standalone schema without Saleor
    if _DASHBOARD_AVAILABLE:
        class Query(InventoryQueries, DashboardQueries, graphene.ObjectType):
            """Query class with inventory and dashboard queries"""
            pass
    else:
        class Query(InventoryQueries, graphene.ObjectType):
            """Query class with inventory queries only"""
            pass
    
    class Mutation(InventoryMutations, graphene.ObjectType):
        """Mutation class with inventory mutations only"""
        pass


# Create the extended schema
schema = graphene.Schema(query=Query, mutation=Mutation)


# Export for use in URLs/views
__all__ = ['schema', 'Query', 'Mutation']
