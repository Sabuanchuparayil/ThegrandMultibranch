#!/bin/bash
# Installation script for Railway deployment
# This script installs Saleor from GitHub and other dependencies

set -e

echo "Upgrading pip..."
pip install --upgrade pip

echo "Installing requirements..."
pip install -r requirements.txt

echo "Installing Saleor from GitHub..."
pip install git+https://github.com/saleor/saleor.git

echo "Installation complete!"

