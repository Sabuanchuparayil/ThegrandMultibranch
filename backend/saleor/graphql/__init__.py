"""
Saleor GraphQL Extensions
This module extends Saleor's GraphQL schema with custom queries and mutations
"""
# Import and expose our extended schema
try:
    from saleor.graphql.schema import schema
    __all__ = ['schema']
except ImportError:
    # Fallback: try to import Saleor's default schema
    try:
        from saleor.graphql import schema
        __all__ = ['schema']
    except ImportError:
        __all__ = []

