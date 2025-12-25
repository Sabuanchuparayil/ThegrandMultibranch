"""
Extended GraphQL Schema for Grand Gold & Diamonds
Extends Saleor's default schema with custom queries and mutations

To use this, you need to configure your GraphQL endpoint to use this schema
instead of Saleor's default schema.
"""
import graphene

# Import Saleor's core schema components
# CRITICAL: Import Saleor's Query and Mutation from core.schema, NOT from graphql.schema
# Importing from graphql.schema would import our own file (circular import)
try:
    # #region agent log
    import json
    import time
    import os
    log_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.cursor', 'debug.log')
    log_dir = os.path.dirname(log_path)
    if not os.path.exists(log_dir):
        log_path = '/tmp/debug.log'
    try:
        with open(log_path, 'a') as f:
            f.write(json.dumps({
                'timestamp': int(time.time() * 1000),
                'location': 'saleor/graphql/schema.py:import_saleor',
                'message': 'Attempting to import Saleor Query and Mutation',
                'data': {'current_file': __file__},
                'sessionId': 'debug-session',
                'runId': 'schema-load',
                'hypothesisId': 'A'
            }) + '\n')
    except:
        pass
    # #endregion
    
    # CRITICAL: Import from core.schema, NOT from graphql.schema
    # graphql.schema would import our own file (circular import)
    # core.schema is Saleor's actual Query/Mutation definitions
    from saleor.graphql.core.schema import Query as SaleorQuery, Mutation as SaleorMutation
    
    # Verify we got the right classes
    print(f"✅ Imported SaleorQuery from: {SaleorQuery.__module__}")
    print(f"✅ Imported SaleorMutation from: {SaleorMutation.__module__}")
    
    # Check if SaleorQuery has the expected fields
    if hasattr(SaleorQuery, '_meta') and hasattr(SaleorQuery._meta, 'fields'):
        saleor_fields = list(SaleorQuery._meta.fields.keys())
        has_products = 'products' in saleor_fields
        has_orders = 'orders' in saleor_fields
        print(f"✅ SaleorQuery has {len(saleor_fields)} fields")
        print(f"   'products' present: {has_products}")
        print(f"   'orders' present: {has_orders}")
        if not has_products or not has_orders:
            print(f"   ⚠️  WARNING: Missing expected Saleor fields. Available: {saleor_fields[:20]}")
    
    _SALEOR_AVAILABLE = True
    print("✅ Saleor Query and Mutation classes imported successfully")
    
    # #region agent log
    try:
        with open(log_path, 'a') as f:
            f.write(json.dumps({
                'timestamp': int(time.time() * 1000),
                'location': 'saleor/graphql/schema.py:import_saleor',
                'message': 'Saleor Query and Mutation imported successfully',
                'data': {
                    'query_module': SaleorQuery.__module__,
                    'mutation_module': SaleorMutation.__module__,
                    'has_products': has_products if 'has_products' in locals() else None,
                    'has_orders': has_orders if 'has_orders' in locals() else None
                },
                'sessionId': 'debug-session',
                'runId': 'schema-load',
                'hypothesisId': 'A'
            }) + '\n')
    except:
        pass
    # #endregion
    
except ImportError as import_error:
    print(f"⚠️  Warning: Saleor schema not available: {import_error}")
    import traceback
    traceback.print_exc()
    _SALEOR_AVAILABLE = False
    SaleorQuery = graphene.ObjectType
    SaleorMutation = graphene.ObjectType
except Exception as e:
    print(f"❌ ERROR importing Saleor schema: {e}")
    import traceback
    traceback.print_exc()
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
    # Wrap fallback creation in error handling to prevent schema from being None
    try:
        class MinimalQuery(graphene.ObjectType):
            pass
        class MinimalMutation(graphene.ObjectType):
            pass
        schema = graphene.Schema(query=MinimalQuery, mutation=MinimalMutation)
        print("⚠️  Created minimal fallback schema")
    except Exception as fallback_error:
        print(f"❌ CRITICAL ERROR: Failed to create even minimal fallback schema: {fallback_error}")
        traceback.print_exc()
        # Last resort: create the most basic schema possible
        # This should never fail unless graphene itself is broken
        try:
            class EmptyQuery(graphene.ObjectType):
                """Empty query type as last resort"""
                pass
            class EmptyMutation(graphene.ObjectType):
                """Empty mutation type as last resort"""
                pass
            schema = graphene.Schema(query=EmptyQuery, mutation=EmptyMutation)
            print("⚠️  Created empty fallback schema as last resort")
        except Exception as final_error:
            # If even this fails, graphene is fundamentally broken
            # Raise an exception to prevent silent failures
            raise RuntimeError(
                f"CRITICAL: Unable to create any GraphQL schema. "
                f"Original error: {e}, Fallback error: {fallback_error}, "
                f"Final error: {final_error}. This indicates a fundamental issue with graphene installation."
            ) from final_error

# Final safety check: ensure schema is never None before export
# This should never trigger due to the error handling above, but provides defense in depth
if schema is None:
    raise RuntimeError(
        "CRITICAL: schema is None after all creation attempts. "
        "This should never happen and indicates a serious configuration issue. "
        "Please check the error logs above for details."
    )

# Export for use in URLs/views
__all__ = ['schema', 'Query', 'Mutation']
