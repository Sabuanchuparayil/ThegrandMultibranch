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


# Import GraphQLView (prefer Saleor's, fall back to graphene-django)
GraphQLView = None
try:
    from saleor.graphql.views import GraphQLView as SaleorGraphQLView

    GraphQLView = SaleorGraphQLView
    print("🔍 [BOOT] grandgold_urls.py: using saleor.graphql.views.GraphQLView")
    _log("grandgold_urls.py:import", "Using saleor.graphql.views.GraphQLView", {}, "H1")
except Exception as e:
    try:
        from graphene_django.views import GraphQLView as DjangoGraphQLView

        GraphQLView = DjangoGraphQLView
        print("🔍 [BOOT] grandgold_urls.py: using graphene_django.views.GraphQLView fallback")
        _log(
            "grandgold_urls.py:import",
            "Using graphene_django.views.GraphQLView fallback",
            {"error": str(e), "error_type": type(e).__name__},
            "H1",
        )
    except Exception as e2:
        print(f"❌ [BOOT] grandgold_urls.py: failed to import GraphQLView ({type(e2).__name__}: {e2})")
        _log(
            "grandgold_urls.py:import",
            "Failed to import any GraphQLView",
            {"error": str(e2), "error_type": type(e2).__name__},
            "H1",
        )


# Import our extended schema (outside saleor.*)
extended_schema = None
try:
    from grandgold_graphql.schema import schema as extended_schema

    print(f"🔍 [BOOT] grandgold_urls.py: imported extended schema from {getattr(extended_schema, '__module__', None)}")
    _log(
        "grandgold_urls.py:schema",
        "Imported extended schema",
        {"schema_module": getattr(extended_schema, "__module__", None)},
        "H3",
    )
except Exception as e:
    print(f"❌ [BOOT] grandgold_urls.py: failed to import extended schema ({type(e).__name__}: {e})")
    _log(
        "grandgold_urls.py:schema",
        "Failed to import extended schema",
        {"error": str(e), "error_type": type(e).__name__, "traceback": traceback.format_exc()},
        "H3",
    )


def _wrap_graphql_view(schema):
    """Add minimal runtime logging around GraphQL view execution."""
    base_view = GraphQLView.as_view(schema=schema)

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
    return JsonResponse(
        {
            "ok": True,
            "urlconf": "grandgold_urls",
            "has_graphql_view": GraphQLView is not None,
            "has_extended_schema": extended_schema is not None,
        }
    )

urlpatterns.append(path("__grandgold__/ping", _ping, name="grandgold_ping"))

# Add our GraphQL override first
if GraphQLView and extended_schema is not None:
    urlpatterns.append(path("graphql/", _wrap_graphql_view(extended_schema), name="extended_graphql"))
    _log("grandgold_urls.py:urlpatterns", "Registered extended /graphql/ endpoint", {}, "H1")
else:
    # Register a fallback endpoint so /graphql/ never 404s; this gives runtime evidence
    def _graphql_fallback(_request):
        return JsonResponse(
            {
                "error": "Extended GraphQL endpoint not available",
                "has_graphql_view": GraphQLView is not None,
                "has_extended_schema": extended_schema is not None,
            },
            status=500,
        )

    urlpatterns.append(path("graphql/", _graphql_fallback, name="extended_graphql_fallback"))
    _log(
        "grandgold_urls.py:urlpatterns",
        "Extended /graphql/ endpoint NOT registered",
        {"has_graphql_view": GraphQLView is not None, "has_schema": extended_schema is not None},
        "H1",
    )


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


