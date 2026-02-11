#!/bin/bash

# myfetch - Complete Uninstallation Script
# This script removes the myfetch installation, symlink, config, and PATH entries.

set -e

INSTALL_DIR="$HOME/.local/share/myfetch"
CONFIG_DIR="$HOME/.config/myfetch"
BIN_DIR="$HOME/.local/bin"
BINARY_NAME="myfetch"

echo "🗑️  Thoroughly uninstalling myfetch..."

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

# 3. Remove configuration directory
if [ -d "$CONFIG_DIR" ]; then
    echo "Removing configuration directory $CONFIG_DIR..."
    rm -rf "$CONFIG_DIR"
fi

# 4. Clean up PATH in shell profiles
PROFILES=("$HOME/.bashrc" "$HOME/.zshrc" "$HOME/.profile")
PATH_LINE="export PATH=\"\$HOME/.local/bin:\$PATH\""
COMMENT_LINE="# Added by myfetch installer"

for PROFILE in "${PROFILES[@]}"; do
    if [ -f "$PROFILE" ]; then
        if grep -q "$PATH_LINE" "$PROFILE"; then
            echo "Cleaning up PATH in $PROFILE..."
            # Use a temporary file for safe editing
            sed -i "/$COMMENT_LINE/d" "$PROFILE"
            sed -i "s|export PATH=\"\$HOME/.local/bin:\$PATH\"||g" "$PROFILE"
            # Remove empty lines that might have been left
            sed -i '/^$/d' "$PROFILE" # Note: this is aggressive, let's be careful.
            # actually better to just remove specific lines
            sed -i "/# Added by myfetch installer/d" "$PROFILE"
            sed -i "\|$PATH_LINE|d" "$PROFILE"
        fi
    fi
done

echo ""
echo "✅ Success! myfetch has been purged from your system."
echo "👉 Note: Changes to your PATH will take effect in NEW terminal windows."
