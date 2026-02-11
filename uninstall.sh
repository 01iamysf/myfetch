#!/bin/bash

# myfetch - Uninstallation Script
# This script removes the myfetch installation and symlink.

set -e

INSTALL_DIR="$HOME/.local/share/myfetch"
BIN_DIR="$HOME/.local/bin"
BINARY_NAME="myfetch"

echo "🗑️  Uninstalling myfetch..."

# 1. Remove the symlink
if [ -L "$BIN_DIR/$BINARY_NAME" ]; then
    echo "Removing symlink from $BIN_DIR..."
    rm "$BIN_DIR/$BINARY_NAME"
fi

# 2. Remove the installation directory
if [ -d "$INSTALL_DIR" ]; then
    echo "Removing installation directory $INSTALL_DIR..."
    rm -rf "$INSTALL_DIR"
fi

echo "✅ Success! myfetch has been uninstalled."
echo "Note: The PATH entry in your shell profile (~/.bashrc or ~/.zshrc) was not removed."
echo "You can manually remove it if you wish."
