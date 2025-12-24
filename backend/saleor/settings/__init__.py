"""
Saleor settings package for Grand Gold & Diamonds

This module extends Saleor's default settings with our custom configurations.

Strategy: We use a direct import approach where we import from the installed
Saleor package's settings module, then apply our extensions.
"""

# Import installed Saleor settings directly
# We use a special import trick: temporarily modify sys.path to prioritize site-packages
import sys
import os

# Save original path
_original_path = sys.path[:]

# Temporarily prepend site-packages to path to ensure we get installed Saleor
# (This is a workaround - normally site-packages is already early in the path)
try:
    import site
    site_packages = [p for p in site.getsitepackages() if 'site-packages' in p]
    if site_packages:
        for sp in site_packages:
            if sp not in sys.path:
                sys.path.insert(0, sp)
except:
    pass

# Now import from installed Saleor package
try:
    # Temporarily remove our local saleor from modules if present
    _had_local_saleor = 'saleor' in sys.modules
    _had_local_settings = 'saleor.settings' in sys.modules
    
    if _had_local_saleor:
        _temp_saleor = sys.modules.pop('saleor')
    if _had_local_settings:
        _temp_settings = sys.modules.pop('saleor.settings')
    
    # Import the installed Saleor settings
    from saleor.settings import *  # noqa: F403, F405
    
    # Restore local modules
    if _had_local_saleor:
        sys.modules['saleor'] = _temp_saleor
    if _had_local_settings:
        sys.modules['saleor.settings'] = _temp_settings
        
except ImportError as e:
    raise ImportError(
        f"Could not import Saleor settings from installed package: {e}. "
        "Make sure Saleor is installed: pip install git+https://github.com/saleor/saleor.git"
    )
finally:
    # Restore original path
    sys.path[:] = _original_path

# Now import our extensions from base.py (which extends the imported settings)
from .base import *  # noqa: F403, F405

# Optionally load local overrides
try:
    from .local import *  # noqa: F403, F405
except ImportError:
    pass
