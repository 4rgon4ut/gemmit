#!/bin/bash

# This script installs the gemmit tool.

# The directory where gemmit will be installed.
INSTALL_DIR="$HOME/.gemmit"
CONFIG_FILE="$INSTALL_DIR/config.json"
SCRIPT_FILE="$INSTALL_DIR/gemmit.py"
GEMMIT_FILE="$INSTALL_DIR/gemmit"

SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/src"

# Create the installation directory if it doesn't exist.
mkdir -p "$INSTALL_DIR"

# Copy the config file and the scripts.
cp "$SOURCE_DIR/config.json" "$CONFIG_FILE"
cp "$SOURCE_DIR/gemmit.py" "$SCRIPT_FILE"
cp "$SOURCE_DIR/gemmit" "$GEMMIT_FILE"

# Copy the new directories
cp -r "$SOURCE_DIR/commands" "$INSTALL_DIR/commands"
cp -r "$SOURCE_DIR/core" "$INSTALL_DIR/core"
cp -r "$SOURCE_DIR/utils" "$INSTALL_DIR/utils"


# Make the scripts executable.
chmod +x "$SCRIPT_FILE"
chmod +x "$GEMMIT_FILE"


echo "gemmit installed successfully!"
echo ""
echo "To use it, add the following line to your shell profile (e.g., ~/.bashrc, ~/.zshrc):"
echo "export PATH=\"$INSTALL_DIR:\$PATH\""

echo ""
echo "To uninstall gemmit, run:"
echo "rm -rf $INSTALL_DIR"