"""
URL Configuration for Grand Gold & Diamonds

This extends Saleor's URLs and adds GraphQL endpoint with custom schema
"""
from django.conf import settings
from django.urls import path, include

# Import our extended GraphQL schema
try:
    from saleor.graphql.schema import schema as extended_schema
    _EXTENDED_SCHEMA_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Extended GraphQL schema not available: {e}")
    _EXTENDED_SCHEMA_AVAILABLE = False
    extended_schema = None

# Try to import GraphQLView - prefer graphene_django as it's more standard
GraphQLView = None
try:
    from graphene_django.views import GraphQLView
    print("✅ Using graphene_django.views.GraphQLView")
except ImportError:
    try:
        from saleor.graphql.views import GraphQLView
        print("✅ Using saleor.graphql.views.GraphQLView")
    except ImportError:
        print("⚠️  Warning: Could not import GraphQLView - GraphQL endpoint may not work")

# Import Saleor URLs
try:
    from saleor.urls import urlpatterns as saleor_urlpatterns
    # Filter out Saleor's /graphql/ path if it exists (we'll use our own)
    saleor_urlpatterns = [
        url_pattern for url_pattern in saleor_urlpatterns
        if not (hasattr(url_pattern, 'pattern') and 
                hasattr(url_pattern.pattern, 'regex') and 
                url_pattern.pattern.regex.pattern == r'^graphql/$')
    ]
except ImportError:
    saleor_urlpatterns = []

# Custom URL patterns
# IMPORTANT: Override GraphQL endpoint BEFORE including Saleor URLs
# This ensures our extended schema is used instead of Saleor's default
urlpatterns = []

# Override GraphQL endpoint with our extended schema (if available)
if _EXTENDED_SCHEMA_AVAILABLE and GraphQLView:
    # Add our extended GraphQL endpoint first (Django uses first match)
    urlpatterns.append(
        path('graphql/', GraphQLView.as_view(schema=extended_schema))
    )
    print("✅ Extended GraphQL schema loaded and endpoint configured")
    print(f"   Schema type: {type(extended_schema)}")
    if hasattr(extended_schema, 'query_type'):
        query_fields = list(extended_schema.query_type._meta.fields.keys()) if hasattr(extended_schema.query_type, '_meta') else []
        branches_in_schema = 'branches' in query_fields
        print(f"   Query fields count: {len(query_fields)}")
        print(f"   'branches' query present: {branches_in_schema}")
        if not branches_in_schema:
            print(f"   Available query fields (first 20): {query_fields[:20]}")
else:
    print("⚠️  Extended GraphQL schema not available, using Saleor default")
    if not _EXTENDED_SCHEMA_AVAILABLE:
        print("   Reason: Extended schema import failed")
    if not GraphQLView:
        print("   Reason: GraphQLView import failed")

# Include Saleor URLs (Saleor's /graphql/ has been filtered out)
urlpatterns.extend(saleor_urlpatterns)

