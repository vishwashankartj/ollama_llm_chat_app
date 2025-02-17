#!/bin/bash

# Create a new virtual environment in the current directory
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Install dependencies from requirements.txt
pip install -r requirements.txt

# Set PYTHONPATH to the current directory
export PYTHONPATH=$(pwd)

# Confirm the setup
echo "Virtual environment created and activated."
echo "Dependencies installed."
echo "PYTHONPATH set to: $PYTHONPATH"
