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

# 5. PATH verification and fix
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo "⚠️  $BIN_DIR is not in your PATH."
    
    SHELL_PROFILE=""
    case "$SHELL" in
        */bash) SHELL_PROFILE="$HOME/.bashrc" ;;
        */zsh)  SHELL_PROFILE="$HOME/.zshrc" ;;
        *)      SHELL_PROFILE="$HOME/.profile" ;;
    esac

    if [ -f "$SHELL_PROFILE" ]; then
        if ! grep -q "$BIN_DIR" "$SHELL_PROFILE"; then
            echo "Adding $BIN_DIR to PATH in $SHELL_PROFILE..."
            echo "" >> "$SHELL_PROFILE"
            echo "# Added by myfetch installer" >> "$SHELL_PROFILE"
            echo "export PATH=\"\$HOME/.local/bin:\$PATH\"" >> "$SHELL_PROFILE"
            
            echo "✅ Success! PATH updated in $SHELL_PROFILE."
            echo ""
            echo "--------------------------------------------------------"
            echo "👉 ATTENTION: YOU MUST RUN THE FOLLOWING COMMAND TO START:"
            echo "   source $SHELL_PROFILE"
            echo "--------------------------------------------------------"
            echo ""
            echo "Or simply restart your terminal."
        else
            echo "PATH export already exists in $SHELL_PROFILE but is not active."
            echo "👉 Please run: source $SHELL_PROFILE"
        fi
    else
        echo "Could not find a shell profile to update."
        echo "Please manually add $BIN_DIR to your PATH."
    fi
else
    echo "✅ Success! You can now run 'myfetch' from any terminal."
fi
