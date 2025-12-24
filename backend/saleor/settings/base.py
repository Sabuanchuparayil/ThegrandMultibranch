"""
Django settings for Grand Gold & Diamonds project.
This extends Saleor's default settings.
"""
# Import Saleor's default settings first
from saleor.settings import *  # noqa: F403, F405

# Extend INSTALLED_APPS with our custom extensions
INSTALLED_APPS = list(INSTALLED_APPS) + [  # noqa: F405
    'saleor_extensions.regions',
    'saleor_extensions.currency',
    'saleor_extensions.branches',
    'saleor_extensions.inventory',
    'saleor_extensions.pricing',
    'saleor_extensions.taxes',
    'saleor_extensions.orders',
    'saleor_extensions.products',
    'saleor_extensions.fulfillment',
    'saleor_extensions.returns',
    'saleor_extensions.customers',
    'saleor_extensions.promotions',
    'saleor_extensions.cms',
    'saleor_extensions.notifications',
    'saleor_extensions.payments',
    'saleor_extensions.invoices',
    'saleor_extensions.reports',
    'saleor_extensions.integrations',
    'saleor_extensions.audit',
    'saleor_extensions.permissions',
]

# Add audit middleware after AuthenticationMiddleware
if 'saleor_extensions.audit.middleware.AuditLogMiddleware' not in MIDDLEWARE:  # noqa: F405
    try:
        auth_index = MIDDLEWARE.index('django.contrib.auth.middleware.AuthenticationMiddleware')  # noqa: F405
        MIDDLEWARE.insert(auth_index + 1, 'saleor_extensions.audit.middleware.AuditLogMiddleware')  # noqa: F405
    except ValueError:
        MIDDLEWARE.append('saleor_extensions.audit.middleware.AuditLogMiddleware')  # noqa: F405
