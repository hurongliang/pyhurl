#!/bin/bash

# Clean up previous builds
rm -rf ./build ./dist ./pyhurl.egg-info

# Install/upgrade build tools
pip install --upgrade pip
pip install --upgrade build twine

# Build the package
python -m build

# Upload to PyPI
twine upload dist/*

# Clean up
rm -rf ./build ./pyhurl.egg-info