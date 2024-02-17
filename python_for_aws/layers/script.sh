#!/bin/bash

# Check if package name is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <package-name>"
    exit 1
fi

PACKAGE_NAME=$1
PYTHON_VERSION=python3.11  # Adjusted for Python 3.11
LAYER_DIR="python/lib/$PYTHON_VERSION/site-packages"

# Create directory structure for the layer
mkdir -p $LAYER_DIR
cd $LAYER_DIR

# Install the package and its dependencies using pip
pip install $PACKAGE_NAME --target .

# Go back to the root directory of the layer
cd - 

# Zip the layer
zip -r ${PACKAGE_NAME}_layer.zip python

echo "Layer package ${PACKAGE_NAME}_layer.zip created successfully."

