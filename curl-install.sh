#!/bin/bash

# myfetch - Remote Install Script
# Usage: curl -sSL https://raw.githubusercontent.com/01iamysf/myfetch/main/curl-install.sh | bash

set -e

REPO_URL="https://github.com/01iamysf/myfetch.git"
INSTALL_DIR="$HOME/.local/bin"
TEMP_DIR=$(mktemp -d)

echo "☁️  Cloning myfetch from GitHub..."
git clone --depth 1 "$REPO_URL" "$TEMP_DIR"

cd "$TEMP_DIR"

echo "🚀 Installing myfetch to $INSTALL_DIR..."
mkdir -p "$INSTALL_DIR"
chmod +x myfetch.py

# Create/Update symlink with absolute path
# We copy the script to a permanent location first if we want it to survive TEMP_DIR deletion
# Or we can just copy it to INSTALL_DIR directly
cp myfetch.py "$INSTALL_DIR/myfetch"
chmod +x "$INSTALL_DIR/myfetch"

# Check if INSTALL_DIR is in PATH
if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
    echo "⚠️  Note: $INSTALL_DIR is not in your PATH."
    echo "Please add the following line to your ~/.bashrc or ~/.zshrc:"
    echo "export PATH=\"\$HOME/.local/bin:\$PATH\""
else
    echo "✅ Success! You can now run 'myfetch' from any terminal."
fi

# Cleanup
rm -rf "$TEMP_DIR"

echo "Try it now with: myfetch --help"
