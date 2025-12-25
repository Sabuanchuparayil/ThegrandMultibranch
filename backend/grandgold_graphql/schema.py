"""
Grand Gold extended GraphQL schema.

IMPORTANT:
- This module intentionally does NOT live under the `saleor.*` package name.
- In production we prefer importing Saleor from site-packages; a local `backend/saleor/`
  folder may not be imported at all. Keeping our extension entrypoint outside `saleor`
  guarantees it can be imported regardless of Saleor import precedence.
"""

import graphene


def _log(location: str, message: str, data: dict, hypothesis_id: str, run_id: str = "schema-debug") -> None:
    # #region agent log
    import json
    import os
    import time

    try:
        log_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".cursor", "debug.log")
        if not os.path.exists(os.path.dirname(log_path)):
            log_path = "/tmp/debug.log"
        with open(log_path, "a") as f:
            f.write(
                json.dumps(
                    {
                        "timestamp": int(time.time() * 1000),
                        "sessionId": "debug-session",
                        "runId": run_id,
                        "hypothesisId": hypothesis_id,
                        "location": location,
                        "message": message,
                        "data": data,
                    }
                )
                + "\n"
            )
    except Exception:
        pass
    # #endregion


_log(
    "grandgold_graphql/schema.py:load",
    "Loading Grand Gold extended schema module",
    {"file": __file__},
    "H3",
)


# --- Import Saleor core schema (installed) ---
# Try to get Saleor's actual schema object first, then extract Query/Mutation
SaleorQuery = None
SaleorMutation = None
_SALEOR_AVAILABLE = False
_SALEOR_SCHEMA_OBJ = None

# Strategy 1: Try to get Saleor's complete schema object
try:
    import sys
    # Remove local saleor.graphql to force import from installed package
    _local_backup = None
    if 'saleor.graphql' in sys.modules:
        _local_backup = sys.modules.pop('saleor.graphql')
    
    try:
        from saleor.graphql import schema as saleor_schema_obj
        _SALEOR_SCHEMA_OBJ = saleor_schema_obj
        
        # Extract Query and Mutation from schema object
        if hasattr(saleor_schema_obj, 'Query'):
            SaleorQuery = saleor_schema_obj.Query
        elif hasattr(saleor_schema_obj, 'schema') and hasattr(saleor_schema_obj.schema, 'query_type'):
            # If schema object has a schema attribute, get Query from there
            SaleorQuery = saleor_schema_obj.schema.query_type._meta.type
        
        if hasattr(saleor_schema_obj, 'Mutation'):
            SaleorMutation = saleor_schema_obj.Mutation
        elif hasattr(saleor_schema_obj, 'schema') and hasattr(saleor_schema_obj.schema, 'mutation_type'):
            SaleorMutation = saleor_schema_obj.schema.mutation_type._meta.type
        
        if SaleorQuery and SaleorMutation:
            _SALEOR_AVAILABLE = True
            print(f"✅ [SCHEMA] Imported SaleorQuery from: {SaleorQuery.__module__}")
            print(f"✅ [SCHEMA] Imported SaleorMutation from: {SaleorMutation.__module__}")
            # Check fields
            if hasattr(SaleorQuery, '_meta') and hasattr(SaleorQuery._meta, 'fields'):
                fields = list(SaleorQuery._meta.fields.keys())
                print(f"✅ [SCHEMA] SaleorQuery has {len(fields)} fields")
                print(f"   Has products: {'products' in fields}")
                print(f"   Has orders: {'orders' in fields}")
                print(f"   Has users: {'users' in fields}")
            _log(
                "grandgold_graphql/schema.py:import_saleor",
                "Imported Saleor schema object (strategy 1)",
                {
                    "query_module": SaleorQuery.__module__ if SaleorQuery else None,
                    "mutation_module": SaleorMutation.__module__ if SaleorMutation else None,
                    "has_schema_obj": _SALEOR_SCHEMA_OBJ is not None,
                },
                "H3",
            )
        else:
            raise ImportError("Could not extract Query/Mutation from Saleor schema object")
    finally:
        if _local_backup:
            sys.modules['saleor.graphql'] = _local_backup
    except Exception as e1:
        print(f"⚠️ [SCHEMA] Strategy 1 failed: {e1}")
    # Strategy 2: Import Query/Mutation directly from core.schema
    try:
        from saleor.graphql.core.schema import Query as SaleorQuery, Mutation as SaleorMutation
        _SALEOR_AVAILABLE = True
        print(f"✅ [SCHEMA] Strategy 2 succeeded - Imported from core.schema")
        print(f"   SaleorQuery module: {SaleorQuery.__module__}")
        if hasattr(SaleorQuery, '_meta') and hasattr(SaleorQuery._meta, 'fields'):
            fields = list(SaleorQuery._meta.fields.keys())
            print(f"   SaleorQuery has {len(fields)} fields")
            print(f"   Has products: {'products' in fields}")
            print(f"   Has orders: {'orders' in fields}")
            print(f"   Has users: {'users' in fields}")
        _log(
            "grandgold_graphql/schema.py:import_saleor",
            "Imported Saleor core schema (strategy 2)",
            {"query_module": SaleorQuery.__module__, "mutation_module": SaleorMutation.__module__},
            "H3",
        )
    except Exception as e2:
        # Strategy 3: Try importing from graphql.schema directly
        try:
            import sys
            _local_backup = None
            if 'saleor.graphql' in sys.modules:
                _local_backup = sys.modules.pop('saleor.graphql')
            try:
                from saleor.graphql.schema import Query as SaleorQuery, Mutation as SaleorMutation
                _SALEOR_AVAILABLE = True
                _log(
                    "grandgold_graphql/schema.py:import_saleor",
                    "Imported Saleor schema (strategy 3)",
                    {"query_module": SaleorQuery.__module__, "mutation_module": SaleorMutation.__module__},
                    "H3",
                )
            finally:
                if _local_backup:
                    sys.modules['saleor.graphql'] = _local_backup
        except Exception as e3:
            print(f"⚠️ [SCHEMA] Strategy 3 failed: {e3}")
            _SALEOR_AVAILABLE = False
            SaleorQuery = None
            SaleorMutation = None
            print(f"❌ [SCHEMA] All import strategies failed!")
            print(f"   Error 1: {e1}")
            print(f"   Error 2: {e2}")
            print(f"   Error 3: {e3}")
            _log(
                "grandgold_graphql/schema.py:import_saleor",
                "Failed to import Saleor core schema (all strategies failed)",
                {
                    "error1": str(e1),
                    "error2": str(e2),
                    "error3": str(e3),
                    "error_type": type(e3).__name__,
                },
                "H3",
            )

# Verify we got valid Query/Mutation classes
if _SALEOR_AVAILABLE and SaleorQuery and SaleorMutation:
    # Check if they have the expected structure
    if hasattr(SaleorQuery, '_meta') and hasattr(SaleorQuery._meta, 'fields'):
        fields = list(SaleorQuery._meta.fields.keys())
        _log(
            "grandgold_graphql/schema.py:verify_saleor",
            "SaleorQuery fields verified",
            {
                "field_count": len(fields),
                "has_products": "products" in fields,
                "has_orders": "orders" in fields,
                "has_users": "users" in fields,
                "sample_fields": fields[:10],
            },
            "H3",
        )


# --- Import our extensions ---
from saleor_extensions.inventory.schema import InventoryQueries, InventoryMutations

try:
    from saleor_extensions.branches.schema import BranchQueries, BranchMutations

    _BRANCHES_AVAILABLE = True
    _log(
        "grandgold_graphql/schema.py:import_branches",
        "Imported branches schema",
        {"available": True},
        "H2",
    )
except Exception as e:
    _BRANCHES_AVAILABLE = False
    BranchQueries = None
    BranchMutations = None
    _log(
        "grandgold_graphql/schema.py:import_branches",
        "Failed to import branches schema",
        {"available": False, "error": str(e), "error_type": type(e).__name__},
        "H2",
    )

try:
    from saleor_extensions.reports.schema import DashboardQueries

    _DASHBOARD_AVAILABLE = True
except Exception:
    _DASHBOARD_AVAILABLE = False
    DashboardQueries = None


# --- Compose schema ---
class GrandGoldQueries(graphene.ObjectType):
    """Always-present marker fields to prove our schema is being served."""

    grandgold_schema_version = graphene.String(description="Grand Gold schema marker/version")

    def resolve_grandgold_schema_version(self, info):
        return "grandgold-extended-v1"


def _unique_bases(bases):
    out = []
    seen = set()
    for b in bases:
        if b is None:
            continue
        if b in seen:
            continue
        # Avoid including graphene.ObjectType directly if we already have ObjectType subclasses
        if b is graphene.ObjectType:
            continue
        seen.add(b)
        out.append(b)
    return out


# Build query bases - ensure SaleorQuery is first if available
query_bases = []
print(f"🔍 [SCHEMA] Building query bases...")
print(f"   _SALEOR_AVAILABLE: {_SALEOR_AVAILABLE}")
print(f"   SaleorQuery is None: {SaleorQuery is None}")
print(f"   SaleorQuery type: {type(SaleorQuery)}")

if _SALEOR_AVAILABLE and SaleorQuery is not None:
    query_bases.append(SaleorQuery)
    print(f"✅ [SCHEMA] Added SaleorQuery to query_bases")
    # Log SaleorQuery fields for debugging
    if hasattr(SaleorQuery, '_meta') and hasattr(SaleorQuery._meta, 'fields'):
        saleor_fields = list(SaleorQuery._meta.fields.keys())
        print(f"✅ [SCHEMA] SaleorQuery has {len(saleor_fields)} fields")
        print(f"   Has products: {'products' in saleor_fields}")
        print(f"   Has orders: {'orders' in saleor_fields}")
        print(f"   Has users: {'users' in saleor_fields}")
        print(f"   Sample Saleor fields: {saleor_fields[:10]}")
        _log(
            "grandgold_graphql/schema.py:compose",
            "SaleorQuery included in schema composition",
            {
                "field_count": len(saleor_fields),
                "has_products": "products" in saleor_fields,
                "has_orders": "orders" in saleor_fields,
                "has_users": "users" in saleor_fields,
            },
            "H4",
        )
    else:
        print(f"⚠️ [SCHEMA] SaleorQuery has no _meta.fields")
        _log(
            "grandgold_graphql/schema.py:compose",
            "SaleorQuery included but has no _meta.fields",
            {},
            "H4",
        )
else:
    print(f"❌ [SCHEMA] SaleorQuery NOT included")
    print(f"   _SALEOR_AVAILABLE: {_SALEOR_AVAILABLE}")
    print(f"   SaleorQuery is None: {SaleorQuery is None}")
    _log(
        "grandgold_graphql/schema.py:compose",
        "SaleorQuery NOT included in schema composition",
        {"saleor_available": _SALEOR_AVAILABLE, "saleor_query_is_none": SaleorQuery is None},
        "H4",
    )

query_bases.extend([InventoryQueries, GrandGoldQueries])
if _BRANCHES_AVAILABLE and BranchQueries is not None:
    query_bases.append(BranchQueries)
if _DASHBOARD_AVAILABLE and DashboardQueries is not None:
    query_bases.append(DashboardQueries)

query_bases = _unique_bases(query_bases)

if not query_bases:
    query_bases = [graphene.ObjectType]

# Use proper class inheritance instead of type() for better compatibility
if len(query_bases) == 1:
    Query = query_bases[0]
else:
    Query = type("Query", tuple(query_bases), {})
    
    # Log final Query class fields
try:
    if hasattr(Query, '_meta') and hasattr(Query._meta, 'fields'):
        final_fields = list(Query._meta.fields.keys())
        print(f"✅ [SCHEMA] Final Query class has {len(final_fields)} fields")
        print(f"   Has products: {'products' in final_fields}")
        print(f"   Has orders: {'orders' in final_fields}")
        print(f"   Has users: {'users' in final_fields}")
        print(f"   Has branches: {'branches' in final_fields}")
        print(f"   Sample fields: {final_fields[:10]}")
        _log(
            "grandgold_graphql/schema.py:final_query",
            "Final Query class created",
            {
                "field_count": len(final_fields),
                "has_products": "products" in final_fields,
                "has_orders": "orders" in final_fields,
                "has_users": "users" in final_fields,
                "has_branches": "branches" in final_fields,
                "sample_fields": final_fields[:15],
            },
            "H4",
        )
    else:
        print("⚠️ [SCHEMA] Final Query class has no _meta.fields")
except Exception as e:
    print(f"❌ [SCHEMA] Could not inspect final Query class: {e}")
    _log(
        "grandgold_graphql/schema.py:final_query",
        "Could not inspect final Query class",
        {"error": str(e)},
        "H4",
    )


# Build mutation bases - ensure SaleorMutation is first if available
mutation_bases = []
if _SALEOR_AVAILABLE and SaleorMutation is not None:
    mutation_bases.append(SaleorMutation)
mutation_bases.append(InventoryMutations)
if _BRANCHES_AVAILABLE and BranchMutations is not None:
    mutation_bases.append(BranchMutations)

mutation_bases = _unique_bases(mutation_bases)

if not mutation_bases:
    mutation_bases = [graphene.ObjectType]

# Use proper class inheritance instead of type() for better compatibility
if len(mutation_bases) == 1:
    Mutation = mutation_bases[0]
else:
    Mutation = type("Mutation", tuple(mutation_bases), {})


try:
    schema = graphene.Schema(query=Query, mutation=Mutation)
    _log(
        "grandgold_graphql/schema.py:create",
        "Schema created successfully",
        {"query_bases_count": len(query_bases), "mutation_bases_count": len(mutation_bases)},
        "H5",
    )
except Exception as e:
    _log(
        "grandgold_graphql/schema.py:create",
        "Schema creation failed",
        {"error": str(e), "error_type": type(e).__name__, "traceback": __import__("traceback").format_exc()},
        "H5",
    )
    raise


def _verify_schema() -> None:
    try:
        fields = []
        if hasattr(schema, "query_type") and hasattr(schema.query_type, "_meta") and hasattr(schema.query_type._meta, "fields"):
            fields = list(schema.query_type._meta.fields.keys())
        _log(
            "grandgold_graphql/schema.py:verify",
            "Extended schema verification",
            {
                "saleor_available": _SALEOR_AVAILABLE,
                "branches_available": _BRANCHES_AVAILABLE,
                "dashboard_available": _DASHBOARD_AVAILABLE,
                "fields_count": len(fields),
                "has_products": "products" in fields,
                "has_orders": "orders" in fields,
                "has_branches": "branches" in fields,
                "has_branch_inventory": "branchInventory" in fields,
                "sample_fields": fields[:60],
            },
            "H3",
        )
    except Exception as e:
        _log(
            "grandgold_graphql/schema.py:verify",
            "Schema verification failed",
            {"error": str(e), "error_type": type(e).__name__},
            "H3",
        )


_verify_schema()


__all__ = ["schema", "Query", "Mutation"]


