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


# Lazily import GraphQLView + schema at request time.
# This avoids AppRegistryNotReady / import-order issues during Django startup.
GraphQLView = None
_graphql_view_import_error = None
_schema_import_error = None


def _get_graphql_view_and_schema():
    """Return (GraphQLView, schema) or raise with detailed error."""
    global GraphQLView, _graphql_view_import_error, _schema_import_error

    # GraphQLView (prefer Saleor's, fall back to graphene-django)
    if GraphQLView is None and _graphql_view_import_error is None:
        try:
            from saleor.graphql.views import GraphQLView as SaleorGraphQLView

            GraphQLView = SaleorGraphQLView
            print("🔍 [BOOT] grandgold_urls.py: using saleor.graphql.views.GraphQLView (lazy)")
            _log("grandgold_urls.py:import", "Using saleor.graphql.views.GraphQLView", {}, "H1", run_id="runtime")
        except Exception as e:
            _graphql_view_import_error = {"error": str(e), "error_type": type(e).__name__}
            try:
                from graphene_django.views import GraphQLView as DjangoGraphQLView

                GraphQLView = DjangoGraphQLView
                _graphql_view_import_error = None
                print("🔍 [BOOT] grandgold_urls.py: using graphene_django.views.GraphQLView fallback (lazy)")
                _log(
                    "grandgold_urls.py:import",
                    "Using graphene_django.views.GraphQLView fallback",
                    {},
                    "H1",
                    run_id="runtime",
                )
            except Exception as e2:
                _graphql_view_import_error = {"error": str(e2), "error_type": type(e2).__name__}

    # Schema
    schema = None
    if _schema_import_error is None:
        try:
            from grandgold_graphql.schema import schema as extended_schema

            schema = extended_schema
        except Exception as e:
            _schema_import_error = {"error": str(e), "error_type": type(e).__name__}

    if GraphQLView is None:
        raise RuntimeError(f"GraphQLView import failed: {_graphql_view_import_error}")
    if schema is None:
        raise RuntimeError(f"Schema import failed: {_schema_import_error}")

    return GraphQLView, schema


extended_schema = None  # kept for ping visibility; resolved lazily per request


def _wrap_graphql_view(schema, view_cls):
    """Add minimal runtime logging around GraphQL view execution."""
    base_view = view_cls.as_view(schema=schema)

    def wrapped(request, *args, **kwargs):
        # #region agent log
        try:
            _log(
                "grandgold_urls.py:graphql",
                "GraphQL request received",
                {
                    "method": request.method,
                    "path": request.path,
                    "schema_module": getattr(schema, "__module__", None),
                },
                "H1",
                run_id="runtime",
            )
        except Exception:
            pass
        # #endregion

        try:
            response = base_view(request, *args, **kwargs)
            # Marker header to prove this wrapper handled the request
            try:
                response["X-Grandgold-Graphql"] = "1"
            except Exception:
                pass
            return response
        except Exception as e:
            _log(
                "grandgold_urls.py:graphql",
                "GraphQL view crashed",
                {"error": str(e), "error_type": type(e).__name__, "traceback": traceback.format_exc()},
                "H1",
                run_id="runtime",
            )
            raise

    return wrapped


urlpatterns = []

# Always-on ping route to prove this URLConf is active
def _ping(_request):
    # Attempt lazy resolution so ping can show current errors
    view_ok = False
    schema_ok = False
    try:
        _view_cls, _schema = _get_graphql_view_and_schema()
        view_ok = _view_cls is not None
        schema_ok = _schema is not None
    except Exception:
        pass
    return JsonResponse(
        {
            "ok": True,
            "urlconf": "grandgold_urls",
            "has_graphql_view": view_ok,
            "has_extended_schema": schema_ok,
            "graphql_view_error": _graphql_view_import_error,
            "schema_error": _schema_import_error,
        }
    )

urlpatterns.append(path("__grandgold__/ping", _ping, name="grandgold_ping"))

# Always register /graphql/ with lazy resolution.
def _graphql_entrypoint(request):
    try:
        view_cls, schema = _get_graphql_view_and_schema()
        return _wrap_graphql_view(schema, view_cls)(request)
    except Exception as e:
        _log(
            "grandgold_urls.py:graphql",
            "Extended GraphQL endpoint not available",
            {
                "error": str(e),
                "error_type": type(e).__name__,
                "graphql_view_error": _graphql_view_import_error,
                "schema_error": _schema_import_error,
            },
            "H1",
            run_id="runtime",
        )
        return JsonResponse(
            {
                "error": "Extended GraphQL endpoint not available",
                "details": {"error": str(e), "error_type": type(e).__name__},
                "graphql_view_error": _graphql_view_import_error,
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


