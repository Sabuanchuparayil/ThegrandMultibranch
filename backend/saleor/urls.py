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
    # CRITICAL: Use importlib to explicitly load our LOCAL schema file
    # This ensures we get our extended schema, not Saleor's default
    import os
    import sys
    import importlib.util
    
    backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    local_schema_path = os.path.join(backend_dir, 'saleor', 'graphql', 'schema.py')
    
    print(f"🔍 CRITICAL: Loading schema from local file: {local_schema_path}")
    print(f"🔍 File exists: {os.path.exists(local_schema_path)}")
    
    if not os.path.exists(local_schema_path):
        raise FileNotFoundError(f"Local schema file not found: {local_schema_path}")
    
    # Remove any existing saleor.graphql.schema from sys.modules to force reload
    modules_to_remove = [k for k in sys.modules.keys() if k.startswith('saleor.graphql.schema')]
    for mod in modules_to_remove:
        print(f"🔍 Removing from cache: {mod}")
        del sys.modules[mod]
    
    # Ensure backend directory is in path
    if backend_dir not in sys.path:
        sys.path.insert(0, backend_dir)
        print(f"🔍 Added backend_dir to sys.path: {backend_dir}")
    
    # Use importlib to explicitly load our local schema file
    spec = importlib.util.spec_from_file_location("saleor.graphql.schema", local_schema_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not create spec from file: {local_schema_path}")
    
    schema_module = importlib.util.module_from_spec(spec)
    # Add to sys.modules with the correct name so imports work
    sys.modules['saleor.graphql.schema'] = schema_module
    spec.loader.exec_module(schema_module)
    
    # Get the schema from the module
    extended_schema = getattr(schema_module, 'schema', None)
    
    if extended_schema is None:
        raise AttributeError("'schema' attribute not found in loaded module")
    
    _EXTENDED_SCHEMA_AVAILABLE = True
    print("✅ Successfully loaded extended GraphQL schema from LOCAL file")
    print(f"   Schema module: {schema_module.__file__}")
    print(f"   Schema type: {type(extended_schema)}")
    
    # Verify it's actually our schema by checking if it has branches
    if hasattr(extended_schema, 'query_type'):
        try:
            query_fields = list(extended_schema.query_type._meta.fields.keys()) if hasattr(extended_schema.query_type, '_meta') else []
            if 'branches' in query_fields:
                print(f"✅ VERIFIED: 'branches' query is present in schema (total fields: {len(query_fields)})")
            else:
                print(f"❌ CRITICAL: 'branches' query NOT found. Available fields: {query_fields[:20]}")
                print(f"   This means the wrong schema is being loaded!")
        except Exception as verify_error:
            print(f"⚠️  Could not verify schema fields: {verify_error}")
    else:
        print("❌ CRITICAL: Schema has no query_type attribute")
        
except Exception as e:
    print(f"❌ CRITICAL ERROR: Failed to load extended GraphQL schema: {e}")
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
# CRITICAL: We must filter out Saleor's /graphql/ endpoint to use our own
saleor_urlpatterns = []
try:
    from saleor.urls import urlpatterns as saleor_urlpatterns_raw
    print(f"🔍 Found {len(saleor_urlpatterns_raw)} URL patterns from Saleor")
    
    # Filter out Saleor's /graphql/ path - use multiple methods to be sure
    filtered_patterns = []
    graphql_patterns_found = []
    
    for url_pattern in saleor_urlpatterns_raw:
        is_graphql = False
        
        # Method 1: Check pattern string
        try:
            if hasattr(url_pattern, 'pattern'):
                pattern_str = str(url_pattern.pattern)
                if 'graphql' in pattern_str.lower():
                    is_graphql = True
                    graphql_patterns_found.append(pattern_str)
        except:
            pass
        
        # Method 2: Check URL name
        try:
            if hasattr(url_pattern, 'name') and url_pattern.name:
                if 'graphql' in str(url_pattern.name).lower():
                    is_graphql = True
        except:
            pass
        
        # Method 3: Check callback/view
        try:
            if hasattr(url_pattern, 'callback'):
                callback_str = str(url_pattern.callback)
                if 'graphql' in callback_str.lower():
                    is_graphql = True
        except:
            pass
        
        if not is_graphql:
            filtered_patterns.append(url_pattern)
        else:
            print(f"🔍 Filtered out GraphQL pattern: {pattern_str if 'pattern_str' in locals() else 'unknown'}")
    
    saleor_urlpatterns = filtered_patterns
    print(f"✅ Loaded {len(saleor_urlpatterns)} URL patterns from Saleor")
    if graphql_patterns_found:
        print(f"   Removed {len(graphql_patterns_found)} GraphQL pattern(s) from Saleor URLs")
    else:
        print(f"   No GraphQL patterns found in Saleor URLs (this is good)")
        
except Exception as e:
    print(f"⚠️  Warning: Could not import Saleor URLs: {e}")
    print(f"   Traceback: {traceback.format_exc()}")
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

