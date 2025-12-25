"""
Grand Gold URL configuration.

IMPORTANT:
- Do not rely on `saleor.urls` module name to be "our" code. In production, Saleor is
  installed from site-packages and local `backend/saleor/` may be ignored.
- This module is outside the `saleor` package name so we can reliably set ROOT_URLCONF
  to this file and guarantee our /graphql/ override is used.
"""

import os
import traceback
from django.http import JsonResponse
from django.urls import path


def _log(location: str, message: str, data: dict, hypothesis_id: str, run_id: str = "schema-debug") -> None:
    # #region agent log
    import json
    import time

    try:
        log_path = os.path.join(os.path.dirname(__file__), ".cursor", "debug.log")
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


print(f"🔍 [BOOT] grandgold_urls.py loaded from {__file__}")
_log("grandgold_urls.py:load", "Loading Grand Gold URLConf", {"file": __file__}, "H1")


_schema_import_error = None


def _get_schema():
    """Return the extended schema (lazy import)."""
    global _schema_import_error
    try:
        from grandgold_graphql.schema import schema as extended_schema

        return extended_schema
    except Exception as e:
        _schema_import_error = {"error": str(e), "error_type": type(e).__name__}
        raise


urlpatterns = []

# Always-on ping route to prove this URLConf is active
def _ping(_request):
    schema_ok = False
    try:
        _get_schema()
        schema_ok = True
    except Exception:
        schema_ok = False
    return JsonResponse(
        {
            "ok": True,
            "urlconf": "grandgold_urls",
            "has_graphql_view": True,  # we serve GraphQL without GraphQLView
            "has_extended_schema": schema_ok,
            "schema_error": _schema_import_error,
        }
    )

urlpatterns.append(path("__grandgold__/ping", _ping, name="grandgold_ping"))

# Always register /graphql/ with lazy resolution.
def _graphql_entrypoint(request):
    try:
        if request.method != "POST":
            return JsonResponse({"error": "Method not allowed"}, status=405)

        schema = _get_schema()

        try:
            import json

            payload = json.loads(request.body.decode("utf-8") or "{}")
        except Exception:
            payload = {}

        query = payload.get("query")
        variables = payload.get("variables")
        operation_name = payload.get("operationName")

        if not query:
            return JsonResponse({"error": "Missing 'query' in request body"}, status=400)

        # Create proper Saleor context for GraphQL execution
        # Saleor's resolvers expect a context with 'app' attribute
        try:
            from saleor.graphql.core.context import SaleorContext
            context = SaleorContext(request=request, app=None)
        except ImportError:
            # Fallback: create a simple context object with app attribute
            class SimpleContext:
                def __init__(self, request):
                    self.request = request
                    self.app = None
            context = SimpleContext(request)
        
        result = schema.execute(
            query,
            variable_values=variables,
            operation_name=operation_name,
            context_value=context,
        )

        errors = None
        if result.errors:
            errors = []
            for err in result.errors:
                try:
                    locations = [{"line": l.line, "column": l.column} for l in (getattr(err, "locations", None) or [])]
                except Exception:
                    locations = None
                errors.append(
                    {
                        "message": str(err),
                        "locations": locations,
                        "path": getattr(err, "path", None),
                    }
                )

        resp = JsonResponse({"data": result.data, "errors": errors} if errors else {"data": result.data}, status=400 if errors else 200)
        resp["X-Grandgold-Graphql"] = "1"
        return resp
    except Exception as e:
        _log(
            "grandgold_urls.py:graphql",
            "Extended GraphQL endpoint not available",
            {
                "error": str(e),
                "error_type": type(e).__name__,
                "schema_error": _schema_import_error,
            },
            "H1",
            run_id="runtime",
        )
        return JsonResponse(
            {
                "error": "Extended GraphQL endpoint not available",
                "details": {"error": str(e), "error_type": type(e).__name__},
                "schema_error": _schema_import_error,
            },
            status=500,
        )


urlpatterns.append(path("graphql/", _graphql_entrypoint, name="extended_graphql"))


# Append Saleor URLs (installed package)
try:
    from saleor.urls import urlpatterns as saleor_patterns

    urlpatterns.extend(saleor_patterns)
    print(f"🔍 [BOOT] grandgold_urls.py: appended saleor.urls patterns (count={len(saleor_patterns)})")
    _log("grandgold_urls.py:urlpatterns", "Appended saleor.urls patterns", {"count": len(saleor_patterns)}, "H1")
except Exception as e:
    print(f"❌ [BOOT] grandgold_urls.py: failed to import saleor.urls ({type(e).__name__}: {e})")
    _log(
        "grandgold_urls.py:urlpatterns",
        "Failed to import saleor.urls patterns",
        {"error": str(e), "error_type": type(e).__name__, "traceback": traceback.format_exc()},
        "H1",
    )


# Final verification of graphql position
try:
    first = str(urlpatterns[0].pattern) if urlpatterns and hasattr(urlpatterns[0], "pattern") else None
    graphql_positions = []
    for i, p in enumerate(urlpatterns):
        try:
            s = str(p.pattern) if hasattr(p, "pattern") else str(p)
            if "graphql" in s.lower():
                graphql_positions.append({"index": i, "pattern": s})
        except Exception:
            pass
    _log(
        "grandgold_urls.py:verify",
        "URLConf verification",
        {"first_pattern": first, "graphql_patterns": graphql_positions[:10], "total_patterns": len(urlpatterns)},
        "H1",
    )
except Exception:
    pass


