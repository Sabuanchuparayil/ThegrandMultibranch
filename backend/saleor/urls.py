"""
URL Configuration for Grand Gold & Diamonds

This extends Saleor's URLs and adds GraphQL endpoint with custom schema
"""
from django.conf import settings
from django.urls import path, include

# Import Saleor URLs
try:
    from saleor.urls import urlpatterns as saleor_urlpatterns
except ImportError:
    saleor_urlpatterns = []

# Custom URL patterns
urlpatterns = [
    # Include Saleor URLs
    *saleor_urlpatterns,
    
    # Add custom GraphQL endpoint (if you want to override Saleor's)
    # path('graphql/', GraphQLView.as_view(schema=extended_schema)),
]

