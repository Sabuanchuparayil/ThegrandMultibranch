"""
Create Django settings file for Saleor integration
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent

# Create saleor directory if it doesn't exist
saleor_dir = BASE_DIR / 'saleor'
saleor_dir.mkdir(exist_ok=True)

settings_dir = saleor_dir / 'settings'
settings_dir.mkdir(exist_ok=True)

# Create __init__.py
init_file = settings_dir / '__init__.py'
if not init_file.exists():
    init_file.write_text('''from .base import *  # noqa: F403, F405

try:
    from .local import *  # noqa: F403, F405
except ImportError:
    pass
''')
    print("✅ Created saleor/settings/__init__.py")

# Create base.py from Saleor's default settings
base_file = settings_dir / 'base.py'
if not base_file.exists():
    # Import Saleor's default settings
    import saleor.settings as saleor_settings
    import inspect
    
    # Get the base settings file content idea
    print("Creating base.py that imports from Saleor...")
    
    base_content = '''"""
Django settings for Grand Gold & Diamonds project.
This extends Saleor's default settings.
"""
import os
from pathlib import Path

# Build paths inside the project
BASE_DIR = Path(__file__).parent.parent.parent

# Import Saleor's default settings
from saleor.settings import *  # noqa: F403, F405

# Add your custom extensions to INSTALLED_APPS
INSTALLED_APPS = list(INSTALLED_APPS) + [  # noqa: F405
    # Your custom extensions
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

# Add audit middleware
if 'saleor_extensions.audit.middleware.AuditLogMiddleware' not in MIDDLEWARE:  # noqa: F405
    # Insert after AuthenticationMiddleware
    try:
        auth_index = MIDDLEWARE.index('django.contrib.auth.middleware.AuthenticationMiddleware')  # noqa: F405
        MIDDLEWARE.insert(auth_index + 1, 'saleor_extensions.audit.middleware.AuditLogMiddleware')  # noqa: F405
    except ValueError:
        # If AuthenticationMiddleware not found, append to end
        MIDDLEWARE.append('saleor_extensions.audit.middleware.AuditLogMiddleware')  # noqa: F405

# Database configuration (override if needed)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.environ.get('DATABASE_NAME', 'grandgold'),
#         'USER': os.environ.get('DATABASE_USER', 'postgres'),
#         'PASSWORD': os.environ.get('DATABASE_PASSWORD', ''),
#         'HOST': os.environ.get('DATABASE_HOST', 'localhost'),
#         'PORT': os.environ.get('DATABASE_PORT', '5432'),
#     }
# }

# Additional settings for your project
# Add any custom settings here
'''
    
    base_file.write_text(base_content)
    print("✅ Created saleor/settings/base.py")
else:
    print("⚠️  saleor/settings/base.py already exists")

# Create local.py template
local_file = settings_dir / 'local.py.example'
if not local_file.exists():
    local_content = '''"""
Local development settings
Copy this file to local.py and configure for your environment
"""
from .base import *  # noqa: F403, F405

# Override settings for local development
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Database (local development)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'grandgold_dev',
#         'USER': 'postgres',
#         'PASSWORD': 'your_password',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }
'''
    local_file.write_text(local_content)
    print("✅ Created saleor/settings/local.py.example")

print("\n✅ Settings structure created!")
print("\nNext steps:")
print("1. Review and update saleor/settings/base.py")
print("2. Copy local.py.example to local.py and configure")
print("3. Update models with ForeignKeys")
print("4. Run migrations")

