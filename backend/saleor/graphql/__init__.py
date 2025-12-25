"""
Saleor GraphQL Extensions
This module extends Saleor's GraphQL schema with custom queries and mutations
"""
import sys
import os

# Debug: Check which schema module is being imported
_current_file = __file__
_current_dir = os.path.dirname(_current_file)
_schema_file = os.path.join(_current_dir, 'schema.py')
print(f"🔍 saleor.graphql.__init__: Current file: {_current_file}")
print(f"🔍 saleor.graphql.__init__: Schema file path: {_schema_file}")
print(f"🔍 saleor.graphql.__init__: Schema file exists: {os.path.exists(_schema_file)}")

# Import and expose our extended schema
# Use relative import to ensure we get our local schema, not the installed one
try:
    # Try relative import first (our local schema)
    from .schema import schema
    print(f"✅ Successfully imported local schema from {_schema_file}")
    print(f"   Schema type: {type(schema)}")
    __all__ = ['schema']
except ImportError as e:
    print(f"❌ Failed to import local schema: {e}")
    import traceback
    traceback.print_exc()
    # Fallback: try to import Saleor's default schema
    try:
        # This will import from installed Saleor package
        import saleor.graphql.schema as saleor_schema_module
        schema = getattr(saleor_schema_module, 'schema', None)
        if schema:
            print("⚠️  Using Saleor's default schema as fallback")
            __all__ = ['schema']
        else:
            print("❌ Saleor's default schema not found")
            __all__ = []
    except ImportError as e2:
        print(f"❌ Failed to import Saleor's default schema: {e2}")
        __all__ = []

