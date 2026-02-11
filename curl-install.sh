#!/bin/bash

# myfetch - Remote Install Script
# Usage: curl -sSL https://raw.githubusercontent.com/01iamysf/myfetch/main/curl-install.sh | bash

set -e

REPO_URL="https://github.com/01iamysf/myfetch.git"
TEMP_DIR=$(mktemp -d)

echo "☁️  Cloning myfetch from GitHub..."
git clone --depth 1 "$REPO_URL" "$TEMP_DIR"

cd "$TEMP_DIR"

echo "🚀 Installing myfetch via pip..."
if command -v pip3 &> /dev/null; then
    python3 -m pip install --user .
elif command -v pip &> /dev/null; then
    pip install --user .
else
    echo "❌ Error: pip is not installed. Please install python3-pip first."
    exit 1
fi

# Determine where pip installed the binary
# Usually ~/.local/bin or /usr/local/bin
INSTALL_DIR=$(python3 -m site --user-base)/bin

# Check if INSTALL_DIR is in PATH
if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
    echo "⚠️  Note: $INSTALL_DIR is not in your PATH."
    echo "Please add the following line to your ~/.bashrc or ~/.zshrc:"
    echo "export PATH=\"$INSTALL_DIR:\$PATH\""
else
    echo "✅ Success! You can now run 'myfetch' from any terminal."
fi

# Cleanup
rm -rf "$TEMP_DIR"

echo "Try it now with: myfetch --help"
