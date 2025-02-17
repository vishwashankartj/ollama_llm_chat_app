#!/bin/bash

# Exit on any error
set -e

# Create a new virtual environment in the current directory
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Upgrade pip, setuptools, and wheel
pip install --upgrade pip setuptools wheel

# Install dependencies from requirements.txt (fallback if SSL fails)
pip install -r requirements.txt

# Set PYTHONPATH to the current directory
export PYTHONPATH=$(pwd)

# Confirm the setup
echo "✅ Virtual environment created and activated."
echo "✅ Dependencies installed."
echo "✅ PYTHONPATH set to: $PYTHONPATH"
