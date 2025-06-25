#!/bin/bash

# This script installs the gemmit tool.

# The directory where gemmit will be installed.
INSTALL_DIR="$HOME/.gemmit"
CONFIG_FILE="$INSTALL_DIR/config.json"
SCRIPT_FILE="$INSTALL_DIR/gemmit.py"
GEMMIT_FILE="$INSTALL_DIR/gemmit"
HOOK_FILE="$INSTALL_DIR/gemmit-hook"
SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/gemmit"

# Create the installation directory if it doesn't exist.
mkdir -p "$INSTALL_DIR"

# Copy the config file and the scripts.
cp "$SOURCE_DIR/config.json" "$CONFIG_FILE"
cp "$SOURCE_DIR/gemmit.py" "$SCRIPT_FILE"
cp "$SOURCE_DIR/gemmit" "$GEMMIT_FILE"
cp "$SOURCE_DIR/gemmit-hook" "$HOOK_FILE"

# Make the scripts executable.
chmod +x "$SCRIPT_FILE"
chmod +x "$GEMMIT_FILE"
chmod +x "$HOOK_FILE"

echo "gemmit installed successfully!"
echo ""
echo "To use it, add the following line to your shell profile (e.g., ~/.bashrc, ~/.zshrc):"
echo "export PATH=\"$INSTALL_DIR:\$PATH\""
echo ""
echo "Then, run this command in your git repository to set up the hook:"
echo "ln -s $HOOK_FILE .git/hooks/prepare-commit-msg"
echo ""
echo "To uninstall gemmit, run:"
echo "rm -rf $INSTALL_DIR"