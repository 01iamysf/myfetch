#!/bin/bash

# myfetch - Direct Install Script
# This script clones the repository and sets up the symlink.

set -e

REPO_URL="https://github.com/01iamysf/myfetch.git"
INSTALL_DIR="$HOME/.local/share/myfetch"
BIN_DIR="$HOME/.local/bin"
BINARY_NAME="myfetch"

echo "🚀 Installing myfetch..."

# 1. Prepare directories
mkdir -p "$BIN_DIR"

# 2. Clone or Update
if [ -d "$INSTALL_DIR" ]; then
    echo "Updating existing installation in $INSTALL_DIR..."
    cd "$INSTALL_DIR" && git pull origin main
else
    echo "Cloning repository to $INSTALL_DIR..."
    git clone "$REPO_URL" "$INSTALL_DIR"
fi

# 3. Set permissions
chmod +x "$INSTALL_DIR/myfetch.py"

# 4. Create symlink
echo "Creating symlink in $BIN_DIR..."
ln -sf "$INSTALL_DIR/myfetch.py" "$BIN_DIR/$BINARY_NAME"

# 5. PATH verification
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo "⚠️  $BIN_DIR is not in your PATH."
    echo "Please add this to your shell profile (~/.bashrc or ~/.zshrc):"
    echo "export PATH=\"\$HOME/.local/bin:\$PATH\""
else
    echo "✅ Success! You can now run 'myfetch' from any terminal."
fi

echo "Try it now: myfetch"
