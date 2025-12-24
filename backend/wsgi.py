"""
WSGI config for Grand Gold & Diamonds project.

This file creates the WSGI application using our custom settings that extend Saleor.
"""

import os
import sys

# Add the backend directory to Python path so our local saleor package is found
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Set Django settings module to use our custom settings that extend Saleor
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grandgold_settings')

# Import Django's WSGI application
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

