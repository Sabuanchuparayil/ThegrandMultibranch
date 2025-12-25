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

# Import branches queries and mutations
try:
    from saleor_extensions.branches.schema import (
        BranchQueries,
        BranchMutations,
    )
    _BRANCHES_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Branches schema not available: {e}")
    _BRANCHES_AVAILABLE = False
    BranchQueries = graphene.ObjectType
    BranchMutations = graphene.ObjectType

# Import dashboard/reports queries
try:
    from saleor_extensions.reports.schema import DashboardQueries
    _DASHBOARD_AVAILABLE = True
except ImportError:
    _DASHBOARD_AVAILABLE = False
    DashboardQueries = graphene.ObjectType


# Extend Query with custom queries
if _SALEOR_AVAILABLE:
    # Build list of query classes to inherit from
    query_classes = [SaleorQuery, InventoryQueries]
    if _BRANCHES_AVAILABLE:
        query_classes.append(BranchQueries)
    if _DASHBOARD_AVAILABLE:
        query_classes.append(DashboardQueries)
    query_classes.append(graphene.ObjectType)
    
    class Query(*query_classes):
        """Extended Query class combining Saleor and custom queries"""
        pass
    
    # Build list of mutation classes to inherit from
    mutation_classes = [SaleorMutation, InventoryMutations]
    if _BRANCHES_AVAILABLE:
        mutation_classes.append(BranchMutations)
    mutation_classes.append(graphene.ObjectType)
    
    class Mutation(*mutation_classes):
        """Extended Mutation class combining Saleor and custom mutations"""
        pass
else:
    # Standalone schema without Saleor
    # Build list of query classes to inherit from
    query_classes = [InventoryQueries]
    if _BRANCHES_AVAILABLE:
        query_classes.append(BranchQueries)
    if _DASHBOARD_AVAILABLE:
        query_classes.append(DashboardQueries)
    query_classes.append(graphene.ObjectType)
    
    class Query(*query_classes):
        """Query class with custom queries"""
        pass
    
    # Build list of mutation classes to inherit from
    mutation_classes = [InventoryMutations]
    if _BRANCHES_AVAILABLE:
        mutation_classes.append(BranchMutations)
    mutation_classes.append(graphene.ObjectType)
    
    class Mutation(*mutation_classes):
        """Mutation class with custom mutations"""
        pass


# Create the extended schema with error handling
schema = None
try:
    schema = graphene.Schema(query=Query, mutation=Mutation)
    print(f"✅ Extended GraphQL schema created - Branches: {_BRANCHES_AVAILABLE}, Dashboard: {_DASHBOARD_AVAILABLE}, Saleor: {_SALEOR_AVAILABLE}")
    
    # Verify branches query is in the schema
    if _BRANCHES_AVAILABLE:
        try:
            query_type = schema.query_type
            if hasattr(query_type, '_meta') and hasattr(query_type._meta, 'fields'):
                if 'branches' in query_type._meta.fields:
                    print("✅ 'branches' query verified in schema")
                else:
                    print("⚠️  WARNING: 'branches' query NOT found in schema fields")
                    print(f"   Available query fields: {list(query_type._meta.fields.keys())[:20]}")
        except Exception as e:
            print(f"⚠️  Error verifying schema: {e}")
            import traceback
            traceback.print_exc()
except Exception as e:
    print(f"❌ ERROR: Failed to create GraphQL schema: {e}")
    import traceback
    traceback.print_exc()
    # Create a minimal schema to prevent import errors
    class MinimalQuery(graphene.ObjectType):
        pass
    class MinimalMutation(graphene.ObjectType):
        pass
    schema = graphene.Schema(query=MinimalQuery, mutation=MinimalMutation)
    print("⚠️  Created minimal fallback schema")

# Export for use in URLs/views
__all__ = ['schema', 'Query', 'Mutation']
