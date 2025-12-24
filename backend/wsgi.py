"""
WSGI config for Grand Gold & Diamonds project.

This file creates the WSGI application using Saleor's WSGI configuration
with our custom settings module.
"""

import os
import sys

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set Django settings module to use our custom settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'saleor.settings.base')

# Import Django's WSGI application
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

