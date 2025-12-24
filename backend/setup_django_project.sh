#!/bin/bash
# Django Project Setup Script for Saleor Integration

set -e

echo "=========================================="
echo "Setting up Django Project Structure"
echo "=========================================="
echo ""

cd "$(dirname "$0")"

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  Activating virtual environment..."
    source venv/bin/activate
fi

# Check if Saleor is installed
if ! python -c "import saleor" 2>/dev/null; then
    echo "❌ Saleor is not installed!"
    exit 1
fi

echo "✅ Saleor is installed"
echo ""

# Create settings directory structure
echo "📁 Creating settings structure..."
mkdir -p saleor/settings

# Create __init__.py for settings
if [ ! -f "saleor/settings/__init__.py" ]; then
    cat > saleor/settings/__init__.py << 'EOF'
from .base import *  # noqa: F403, F405

try:
    from .local import *  # noqa: F403, F405
except ImportError:
    pass
EOF
    echo "✅ Created saleor/settings/__init__.py"
fi

# Create base.py settings
if [ ! -f "saleor/settings/base.py" ]; then
    echo "⚠️  Creating saleor/settings/base.py - you'll need to configure this"
    echo "   See saleor_settings_integration.py for reference"
fi

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Configure saleor/settings/base.py (see saleor_settings_integration.py)"
echo "2. Create saleor/settings/local.py for local settings"
echo "3. Update models with ForeignKeys"
echo "4. Run migrations"

