#!/bin/bash
# Saleor Installation Script
# This script helps install and set up Saleor for integration

echo "=========================================="
echo "Saleor Integration Setup"
echo "=========================================="
echo ""

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  Virtual environment not activated!"
    echo "Please activate your virtual environment first:"
    echo "  source venv/bin/activate"
    exit 1
fi

echo "✅ Virtual environment detected: $VIRTUAL_ENV"
echo ""

# Install Saleor
echo "📦 Installing Saleor..."
pip install saleor>=3.20.0

if [ $? -eq 0 ]; then
    echo "✅ Saleor installed successfully"
else
    echo "❌ Failed to install Saleor"
    exit 1
fi

echo ""
echo "📋 Next Steps:"
echo "1. Initialize Saleor project (if not already done):"
echo "   Follow: https://docs.saleor.io/docs/3.x/developer/installation"
echo ""
echo "2. Update settings.py:"
echo "   - Add your apps to INSTALLED_APPS"
echo "   - See: saleor_settings_template.py"
echo ""
echo "3. Update models with ForeignKeys:"
echo "   - Follow: MODEL_UPDATES.md"
echo ""
echo "4. Run migrations:"
echo "   python manage.py makemigrations"
echo "   python manage.py migrate"
echo ""
echo "=========================================="
echo "Installation Complete!"
echo "=========================================="


