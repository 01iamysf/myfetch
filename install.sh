#!/bin/bash

# myfetch - Quick Install Script
# This script symlinks the myfetch utility to ~/.local/bin for easy access.

set -e

INSTALL_DIR="$HOME/.local/bin"
PROJECT_DIR="$(pwd)"
SCRIPT_NAME="myfetch"

echo "🚀 Installing myfetch to $INSTALL_DIR..."

# Create directory if it doesn't exist
mkdir -p "$INSTALL_DIR"

# Ensure the script is executable
chmod +x "$PROJECT_DIR/myfetch.py"

# Create/Update symlink
# Use absolute path for the symlink target
ln -sf "$PROJECT_DIR/myfetch.py" "$INSTALL_DIR/$SCRIPT_NAME"

# Check if INSTALL_DIR is in PATH
if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
    echo "⚠️  Note: $INSTALL_DIR is not in your PATH."
    echo "Please add the following line to your ~/.bashrc or ~/.zshrc:"
    echo "export PATH=\"\$HOME/.local/bin:\$PATH\""
else
    echo "✅ Success! You can now run 'myfetch' from any terminal."
fi

echo "Try it now with: myfetch --help"
