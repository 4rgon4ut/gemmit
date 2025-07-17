#!/bin/bash

# This script installs the gemmit tool.

# The directory where gemmit will be installed.
INSTALL_DIR="$HOME/.gemmit"

SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Create the installation directory if it doesn't exist.
mkdir -p "$INSTALL_DIR"

# Remove old cache files
find "$INSTALL_DIR" -type d -name "__pycache__" -exec rm -r {} +

# Copy the application files.
cp -r "$SOURCE_DIR/src/"* "$INSTALL_DIR/"

# Create __init__.py files to make directories importable
find "$INSTALL_DIR" -type d -exec touch {}/__init__.py \;

# Install dependencies
if [ -f "$SOURCE_DIR/requirements.txt" ]; then
    pip install --target="$INSTALL_DIR" -r "$SOURCE_DIR/requirements.txt"
fi

# Make the main script executable.
chmod +x "$INSTALL_DIR/gemmit"

echo "gemmit installed successfully!"
echo ""
echo "To use it, add the following line to your shell profile (e.g., ~/.bashrc, ~/.zshrc):"
echo "export PATH=\"$INSTALL_DIR:\$PATH\""
echo "export PYTHONPATH=\"$INSTALL_DIR:\$PYTHONPATH\""

echo ""
echo "To uninstall gemmit, run:"
echo "rm -rf $INSTALL_DIR"
