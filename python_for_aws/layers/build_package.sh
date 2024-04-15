#!/bin/bash

# Check if package name is provided
if [ -z "$PACKAGE_NAME" ]; then
    echo "Error: Package name not provided."
    exit 1
fi

# Check if Python version is provided, otherwise, use default
if [ -z "$PYTHON_VERSION" ]; then
    PYTHON_VERSION=python3.11
fi

LAYER_DIR="python/lib/$PYTHON_VERSION/site-packages"

# Create directory structure for the layer
mkdir -p $LAYER_DIR
cd $LAYER_DIR || exit

# Install the package and its dependencies using pip
pip install "$PACKAGE_NAME" --target .

# Go back to the root directory of the layer
cd - || exit

# Zip the layer
zip -r "${PACKAGE_NAME}_layer.zip" python

echo "Layer package ${PACKAGE_NAME}_layer.zip created successfully."