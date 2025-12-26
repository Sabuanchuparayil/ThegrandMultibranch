#!/bin/bash
# Python Version Upgrade Script for Saleor

set -e

echo "=========================================="
echo "Python Version Upgrade for Saleor"
echo "=========================================="
echo ""

# Check current Python version
CURRENT_PYTHON=$(python3 --version 2>&1 | awk '{print $2}')
echo "Current Python version: $CURRENT_PYTHON"
echo ""

# Check if Python 3.12 is needed
REQUIRED_VERSION="3.12"
if python3 -c "import sys; exit(0 if sys.version_info >= (3, 12) else 1)" 2>/dev/null; then
    echo "✅ Python version is already compatible with Saleor!"
    exit 0
fi

echo "⚠️  Saleor requires Python 3.12 or higher"
echo ""

# Check for pyenv
if command -v pyenv &> /dev/null; then
    echo "Found pyenv! Recommended approach:"
    echo ""
    echo "1. Install Python 3.12:"
    echo "   pyenv install 3.12.7"
    echo ""
    echo "2. Set local version:"
    echo "   cd $(pwd)"
    echo "   pyenv local 3.12.7"
    echo ""
    echo "3. Recreate virtual environment:"
    echo "   rm -rf venv"
    echo "   python3 -m venv venv"
    echo "   source venv/bin/activate"
    echo ""
    echo "4. Reinstall dependencies:"
    echo "   pip install --upgrade pip"
    echo "   pip install -r requirements.txt"
    echo ""
elif [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    if command -v brew &> /dev/null; then
        echo "Found Homebrew! Recommended approach:"
        echo ""
        echo "1. Install Python 3.12:"
        echo "   brew install python@3.12"
        echo ""
        echo "2. Recreate virtual environment:"
        echo "   cd $(pwd)"
        echo "   rm -rf venv"
        echo "   python3.12 -m venv venv"
        echo "   source venv/bin/activate"
        echo ""
        echo "3. Reinstall dependencies:"
        echo "   pip install --upgrade pip"
        echo "   pip install -r requirements.txt"
        echo ""
    else
        echo "Please install Python 3.12 manually:"
        echo "  Visit: https://www.python.org/downloads/"
        echo ""
    fi
else
    echo "Please install Python 3.12 manually:"
    echo "  Visit: https://www.python.org/downloads/"
    echo ""
fi

echo "=========================================="
echo "After upgrading Python, run:"
echo "  ./install_saleor.sh"
echo "=========================================="


