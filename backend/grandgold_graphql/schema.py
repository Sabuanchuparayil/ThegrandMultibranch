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
try:
    from saleor.graphql.core.schema import Query as SaleorQuery, Mutation as SaleorMutation

    _SALEOR_AVAILABLE = True
    _log(
        "grandgold_graphql/schema.py:import_saleor",
        "Imported Saleor core schema",
        {"query_module": SaleorQuery.__module__, "mutation_module": SaleorMutation.__module__},
        "H3",
    )
except Exception as e:
    _SALEOR_AVAILABLE = False
    # IMPORTANT: Do NOT fall back to graphene.ObjectType here.
    # If we include graphene.ObjectType alongside other graphene.ObjectType subclasses,
    # Python can hit an MRO resolution error. We instead omit SaleorQuery/SaleorMutation
    # entirely when Saleor import fails.
    SaleorQuery = None
    SaleorMutation = None
    _log(
        "grandgold_graphql/schema.py:import_saleor",
        "Failed to import Saleor core schema",
        {"error": str(e), "error_type": type(e).__name__},
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


query_bases = _unique_bases([SaleorQuery, InventoryQueries, GrandGoldQueries])
if _BRANCHES_AVAILABLE:
    query_bases = _unique_bases(query_bases + [BranchQueries])
if _DASHBOARD_AVAILABLE:
    query_bases = _unique_bases(query_bases + [DashboardQueries])

if not query_bases:
    query_bases = [graphene.ObjectType]


Query = type("Query", tuple(query_bases), {})


mutation_bases = _unique_bases([SaleorMutation, InventoryMutations])
if _BRANCHES_AVAILABLE:
    mutation_bases = _unique_bases(mutation_bases + [BranchMutations])

if not mutation_bases:
    mutation_bases = [graphene.ObjectType]

Mutation = type("Mutation", tuple(mutation_bases), {})


schema = graphene.Schema(query=Query, mutation=Mutation)


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


