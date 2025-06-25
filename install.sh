#!/bin/bash

# This script installs the gemmits tool.

# The directory where gemmits will be installed.
INSTALL_DIR="$HOME/.gemmits"
CONFIG_FILE="$INSTALL_DIR/config.json"
SCRIPT_FILE="$INSTALL_DIR/gemmits.py"
SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/gemmits"

# Create the installation directory if it doesn't exist.
mkdir -p "$INSTALL_DIR"

# Copy the config file and the script.
cp "$SOURCE_DIR/config.json" "$CONFIG_FILE"
cp "$SOURCE_DIR/gemmits.py" "$SCRIPT_FILE"

# Make the script executable.
chmod +x "$SCRIPT_FILE"

echo "gemmits installed successfully!"
echo ""
echo "To use it, run this command in your git repository:"
echo "ln -s $SCRIPT_FILE .git/hooks/prepare-commit-msg"
echo ""
echo "To uninstall gemmits, run:"
echo "rm -rf $INSTALL_DIR"