"""
URL Configuration for Grand Gold & Diamonds

This extends Saleor's URLs and adds GraphQL endpoint with custom schema
"""
import traceback
from django.conf import settings
from django.urls import path, include

# Import our extended GraphQL schema with comprehensive error handling
# Note: Python will import from our local saleor/ directory if it's in sys.path before site-packages
extended_schema = None
_EXTENDED_SCHEMA_AVAILABLE = False

try:
    # Import from our local saleor.graphql.schema
    # First, verify we're importing from the right location
    import os
    import sys
    backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    local_schema_path = os.path.join(backend_dir, 'saleor', 'graphql', 'schema.py')
    
    # Ensure backend directory is in path (should already be from wsgi.py)
    if backend_dir not in sys.path:
        sys.path.insert(0, backend_dir)
    
    print(f"🔍 Attempting to import schema from: {local_schema_path}")
    print(f"🔍 File exists: {os.path.exists(local_schema_path)}")
    print(f"🔍 Backend dir in sys.path: {backend_dir in sys.path}")
    
    # Import from our local saleor.graphql.schema
    # This should work because our backend directory is in Python path
    from saleor.graphql.schema import schema as extended_schema
    _EXTENDED_SCHEMA_AVAILABLE = True
    print("✅ Successfully imported extended GraphQL schema")
    print(f"   Schema module: {extended_schema.__module__ if hasattr(extended_schema, '__module__') else 'unknown'}")
    print(f"   Schema type: {type(extended_schema)}")
    
    # Verify it's actually our schema by checking if it has branches
    if hasattr(extended_schema, 'query_type'):
        try:
            query_fields = list(extended_schema.query_type._meta.fields.keys()) if hasattr(extended_schema.query_type, '_meta') else []
            if 'branches' in query_fields:
                print("✅ Verified: 'branches' query is present in imported schema")
            else:
                print(f"⚠️  WARNING: 'branches' query NOT found. Available fields: {query_fields[:10]}")
        except:
            pass
except Exception as e:
    print(f"❌ ERROR: Failed to import extended GraphQL schema: {e}")
    print(f"   Error type: {type(e).__name__}")
    print(f"   Traceback: {traceback.format_exc()}")
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

# Import Saleor URLs with error handling
saleor_urlpatterns = []
try:
    from saleor.urls import urlpatterns as saleor_urlpatterns
    # Filter out Saleor's /graphql/ path if it exists (we'll use our own)
    # Use a safer filtering approach
    filtered_patterns = []
    for url_pattern in saleor_urlpatterns:
        # Check if this is a graphql path by examining the pattern
        is_graphql = False
        try:
            if hasattr(url_pattern, 'pattern'):
                pattern_str = str(url_pattern.pattern)
                if 'graphql' in pattern_str.lower():
                    is_graphql = True
        except:
            pass
        if not is_graphql:
            filtered_patterns.append(url_pattern)
    saleor_urlpatterns = filtered_patterns
    print(f"✅ Loaded {len(saleor_urlpatterns)} URL patterns from Saleor (graphql filtered out)")
except Exception as e:
    print(f"⚠️  Warning: Could not import Saleor URLs: {e}")
    saleor_urlpatterns = []

# Custom URL patterns
# IMPORTANT: Override GraphQL endpoint BEFORE including Saleor URLs
# This ensures our extended schema is used instead of Saleor's default
urlpatterns = []

# Override GraphQL endpoint with our extended schema (if available)
if _EXTENDED_SCHEMA_AVAILABLE and GraphQLView and extended_schema:
    try:
        # Create the GraphQL view with our extended schema
        # Add our extended GraphQL endpoint first (Django uses first match)
        urlpatterns.append(
            path('graphql/', GraphQLView.as_view(schema=extended_schema))
        )
        print("✅ Extended GraphQL schema loaded and endpoint configured")
        print(f"   Schema type: {type(extended_schema)}")
        print(f"   Schema file location: {getattr(extended_schema, '__module__', 'unknown')}")
        if hasattr(extended_schema, 'query_type'):
            try:
                query_fields = list(extended_schema.query_type._meta.fields.keys()) if hasattr(extended_schema.query_type, '_meta') else []
                branches_in_schema = 'branches' in query_fields
                print(f"   Query fields count: {len(query_fields)}")
                print(f"   'branches' query present: {branches_in_schema}")
                if not branches_in_schema:
                    print(f"   Available query fields (first 20): {query_fields[:20]}")
            except Exception as e:
                print(f"   ⚠️  Could not verify schema fields: {e}")
    except Exception as e:
        print(f"❌ ERROR: Failed to configure GraphQL endpoint: {e}")
        print(f"   Traceback: {traceback.format_exc()}")
else:
    print("⚠️  Extended GraphQL schema not available, using Saleor default")
    if not _EXTENDED_SCHEMA_AVAILABLE:
        print("   Reason: Extended schema import failed")
    if not GraphQLView:
        print("   Reason: GraphQLView import failed")
    if not extended_schema:
        print("   Reason: extended_schema is None")

# Include Saleor URLs (Saleor's /graphql/ has been filtered out)
urlpatterns.extend(saleor_urlpatterns)
print(f"✅ Total URL patterns configured: {len(urlpatterns)}")

