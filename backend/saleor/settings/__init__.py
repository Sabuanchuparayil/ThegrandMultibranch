"""
Saleor settings package for Grand Gold & Diamonds

This package extends Saleor's default settings when Saleor is installed as a package.
It imports all settings from Saleor and then applies our custom extensions.
"""

# Import Saleor's default settings first
# When Saleor is installed from GitHub as a package, it provides saleor.settings module
from saleor.settings import *  # noqa: F403, F405

# Now apply our custom extensions from base.py
from .base import *  # noqa: F403, F405

# Optionally load local overrides
try:
    from .local import *  # noqa: F403, F405
except ImportError:
    # local.py doesn't exist or couldn't be imported - that's okay
    pass
