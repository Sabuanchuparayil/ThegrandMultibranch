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
    # CRITICAL FIX: First ensure Saleor's core modules are imported
    # This is necessary for our schema to properly extend Saleor's types
    import os
    import sys
    
    backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    if backend_dir not in sys.path:
        sys.path.insert(0, backend_dir)
    
    # Ensure Saleor's graphql.core is imported first (needed for Product, ProductVariant types)
    try:
        import saleor.graphql.core
        print("✅ Saleor graphql.core imported successfully")
    except Exception as core_error:
        print(f"⚠️  Warning: Could not import saleor.graphql.core: {core_error}")
    
    # Now import our extended schema using standard import (not importlib)
    # The sys.path manipulation above ensures we get our local schema
    # But we need to be careful about module caching
    local_schema_path = os.path.join(backend_dir, 'saleor', 'graphql', 'schema.py')
    print(f"🔍 Attempting to import schema from: {local_schema_path}")
    print(f"🔍 File exists: {os.path.exists(local_schema_path)}")
    
    # Remove our local schema from cache if it exists, to force fresh import
    modules_to_remove = [k for k in list(sys.modules.keys()) if k == 'saleor.graphql.schema']
    for mod in modules_to_remove:
        print(f"🔍 Removing from cache: {mod}")
        del sys.modules[mod]
    
    # Also ensure saleor.graphql is imported (needed for proper module resolution)
    if 'saleor.graphql' not in sys.modules:
        try:
            import saleor.graphql
            print("✅ saleor.graphql module imported")
        except:
            pass
    
    # Now import our schema - Python should use our local file since backend_dir is first in path
    from saleor.graphql.schema import schema as extended_schema
    
    _EXTENDED_SCHEMA_AVAILABLE = True
    print("✅ Successfully imported extended GraphQL schema")
    print(f"   Schema module: {extended_schema.__module__ if hasattr(extended_schema, '__module__') else 'unknown'}")
    print(f"   Schema type: {type(extended_schema)}")
    
    # Verify it's actually our schema by checking if it has branches AND Saleor fields
    if hasattr(extended_schema, 'query_type'):
        try:
            query_fields = list(extended_schema.query_type._meta.fields.keys()) if hasattr(extended_schema.query_type, '_meta') else []
            
            # Check for both our custom fields and Saleor's default fields
            has_branches = 'branches' in query_fields
            has_products = 'products' in query_fields  # Saleor's default
            has_orders = 'orders' in query_fields  # Saleor's default
            
            print(f"   Query fields count: {len(query_fields)}")
            print(f"   'branches' query present: {has_branches}")
            print(f"   'products' query present: {has_products} (Saleor default)")
            print(f"   'orders' query present: {has_orders} (Saleor default)")
            
            if has_branches and has_products:
                print(f"✅ VERIFIED: Schema has both custom ('branches') and Saleor ('products') queries")
            elif has_branches and not has_products:
                print(f"⚠️  WARNING: Schema has 'branches' but missing Saleor's 'products' query")
                print(f"   Available fields: {query_fields[:30]}")
            elif not has_branches:
                print(f"❌ CRITICAL: 'branches' query NOT found. Available fields: {query_fields[:30]}")
        except Exception as verify_error:
            print(f"⚠️  Could not verify schema fields: {verify_error}")
            import traceback
            traceback.print_exc()
    else:
        print("❌ CRITICAL: Schema has no query_type attribute")
        
except Exception as e:
    print(f"❌ CRITICAL ERROR: Failed to import extended GraphQL schema: {e}")
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
        # Create a wrapper view that logs which schema is being used at runtime
        def create_graphql_view_with_logging(schema):
            """Create GraphQL view with runtime logging to verify schema usage"""
            base_view = GraphQLView.as_view(schema=schema)
            
            def wrapped_view(request, *args, **kwargs):
                """Wrapper that logs schema usage for debugging"""
                # #region agent log
                import json
                import time
                import os
                log_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.cursor', 'debug.log')
                log_dir = os.path.dirname(log_path)
                if not os.path.exists(log_dir):
                    log_path = '/tmp/debug.log'
                try:
                    query_fields_list = []
                    has_branches = False
                    if hasattr(schema, 'query_type'):
                        try:
                            query_fields_list = list(schema.query_type._meta.fields.keys()) if hasattr(schema.query_type, '_meta') else []
                            has_branches = 'branches' in query_fields_list
                        except:
                            pass
                    
                    with open(log_path, 'a') as f:
                        f.write(json.dumps({
                            'timestamp': int(time.time() * 1000),
                            'location': 'saleor/urls.py:wrapped_view',
                            'message': 'GraphQL request received',
                            'data': {
                                'method': request.method,
                                'path': request.path,
                                'schema_module': getattr(schema, '__module__', 'unknown'),
                                'has_query_type': hasattr(schema, 'query_type'),
                                'query_fields_count': len(query_fields_list),
                                'has_branches': has_branches,
                                'first_10_fields': query_fields_list[:10] if query_fields_list else []
                            },
                            'sessionId': 'debug-session',
                            'runId': 'runtime',
                            'hypothesisId': 'A'
                        }) + '\n')
                except:
                    pass
                # #endregion
                
                # Log schema info to console for Railway logs
                print(f"🔍 [RUNTIME] GraphQL request - Schema: {getattr(schema, '__module__', 'unknown')}")
                if hasattr(schema, 'query_type'):
                    try:
                        query_fields = list(schema.query_type._meta.fields.keys()) if hasattr(schema.query_type, '_meta') else []
                        has_branches = 'branches' in query_fields
                        print(f"🔍 [RUNTIME] Schema has {len(query_fields)} fields, 'branches' present: {has_branches}")
                        if not has_branches:
                            print(f"🔍 [RUNTIME] Available fields: {query_fields[:30]}")
                    except Exception as e:
                        print(f"🔍 [RUNTIME] Error checking fields: {e}")
                
                return base_view(request, *args, **kwargs)
            
            return wrapped_view
        
        # Create the GraphQL view with our extended schema and logging
        graphql_view = create_graphql_view_with_logging(extended_schema)
        
        # Add our extended GraphQL endpoint first (Django uses first match)
        urlpatterns.append(
            path('graphql/', graphql_view)
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

