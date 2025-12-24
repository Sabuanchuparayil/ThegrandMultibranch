#!/bin/bash
# Build script for Railway deployment
set -e

echo "=== Building Grand Gold Backend ==="

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip setuptools wheel

# Install requirements (without Saleor)
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Install Saleor from GitHub
echo "Installing Saleor from GitHub..."
pip install git+https://github.com/saleor/saleor.git

echo "=== Build complete ==="

