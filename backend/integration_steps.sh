#!/bin/bash
# Step-by-step Saleor Integration Script
# Run each step manually and verify before proceeding

set -e  # Exit on error

echo "=========================================="
echo "Saleor Integration Steps"
echo "=========================================="
echo ""

# Step 1: Check Saleor Installation
echo "STEP 1: Checking Saleor Installation..."
if python3 -c "import saleor" 2>/dev/null; then
    SALEOR_VERSION=$(python3 -c "import saleor; print(saleor.__version__)" 2>/dev/null || echo "installed")
    echo "✅ Saleor is installed (version: $SALEOR_VERSION)"
else
    echo "❌ Saleor is NOT installed"
    echo ""
    echo "Please run:"
    echo "  pip install saleor>=3.20.0"
    echo ""
    read -p "Press Enter after installing Saleor, or Ctrl+C to exit..."
fi

echo ""
echo "STEP 2: Check Django Project Structure"
if [ -d "saleor" ]; then
    echo "✅ Saleor directory exists"
    if [ -f "saleor/settings/base.py" ] || [ -f "saleor/settings/__init__.py" ]; then
        echo "✅ Saleor settings found"
    else
        echo "⚠️  Saleor settings not found - you may need to initialize Saleor"
    fi
else
    echo "❌ Saleor directory not found"
    echo "You need to initialize Saleor project structure"
    echo "See: https://docs.saleor.io/docs/3.x/developer/installation"
    exit 1
fi

echo ""
echo "STEP 3: Check Extensions"
if [ -d "saleor_extensions" ]; then
    APP_COUNT=$(find saleor_extensions -mindepth 1 -maxdepth 1 -type d ! -name "__pycache__" | wc -l)
    echo "✅ Found $APP_COUNT extension apps"
else
    echo "❌ saleor_extensions directory not found"
    exit 1
fi

echo ""
echo "=========================================="
echo "READY FOR INTEGRATION"
echo "=========================================="
echo ""
echo "Next Steps:"
echo "1. Update saleor/settings/base.py with your apps (see saleor_settings_integration.py)"
echo "2. Update models with ForeignKeys (see MODEL_UPDATES.md)"
echo "3. Run: python manage.py makemigrations"
echo "4. Run: python manage.py migrate"
echo "5. Run: python manage.py shell < create_initial_data.py"
echo "6. Test in Django admin"
echo ""
echo "For detailed instructions, see:"
echo "  - SALEOR_INTEGRATION_GUIDE.md"
echo "  - MODEL_UPDATES.md"
echo "  - INTEGRATION_CHECKLIST.md"

