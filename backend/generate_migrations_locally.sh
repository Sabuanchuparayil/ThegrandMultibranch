#!/bin/bash
# Script to generate migrations locally
# Run this on your local machine before deploying

set -e

echo "=========================================="
echo "Generating Django Migrations Locally"
echo "=========================================="
echo ""

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found. Please create one first:"
    echo "   python3 -m venv .venv"
    echo "   source .venv/bin/activate"
    echo "   pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source .venv/bin/activate

# Check if Django is installed
if ! python -c "import django" 2>/dev/null; then
    echo "❌ Django not found. Please install dependencies:"
    echo "   pip install -r requirements.txt"
    exit 1
fi

# Set Django settings
export DJANGO_SETTINGS_MODULE=grandgold_settings

# Generate migrations for each app
echo ""
echo "🔨 Generating migrations..."
echo ""

APPS=("regions" "currency" "branches" "inventory")

for app in "${APPS[@]}"; do
    echo "📝 Creating migrations for: $app"
    python manage.py makemigrations "$app" || {
        echo "⚠️  Warning: Failed to create migrations for $app"
        echo "   This might be OK if migrations already exist"
    }
done

echo ""
echo "✅ Migration generation complete!"
echo ""
echo "📋 Review the generated migration files:"
for app in "${APPS[@]}"; do
    if [ -d "saleor_extensions/$app/migrations" ]; then
        echo "   saleor_extensions/$app/migrations/"
    fi
done

echo ""
echo "🧪 Test migrations locally:"
echo "   python manage.py migrate"
echo ""
echo "📤 Commit and push migration files:"
echo "   git add saleor_extensions/*/migrations/"
echo "   git commit -m 'Add migration files'"
echo "   git push"
echo ""

