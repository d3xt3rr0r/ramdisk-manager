#!/usr/bin/env bash

SCRIPT_PATH="$HOME/.config/ramdisk-manager/ramdisk.py"
WRAPPER_PATH="$HOME/.local/bin/ramdisk-manager"

# ---------------- INSTALL WRAPPER ----------------
install_wrapper() {
    mkdir -p "$HOME/.local/bin"

    if [ ! -f "$WRAPPER_PATH" ]; then
        cat > "$WRAPPER_PATH" << EOF
#!/usr/bin/env bash
python3 "$SCRIPT_PATH" "\$@"
EOF
        chmod +x "$WRAPPER_PATH"
        echo "Wrapper installed: $WRAPPER_PATH"
    fi

    if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
        echo "Warning: ~/.local/bin is not in PATH"
        echo "Add this to your shell config (~/.bashrc, ~/.zshrc):"
        echo 'export PATH="$HOME/.local/bin:$PATH"'
    fi
}

# ---------------- MAIN ----------------

install_wrapper

if [ ! -f "$SCRIPT_PATH" ]; then
    echo "Error: ramdisk.py not found at $SCRIPT_PATH"
    exit 1
fi
if [ -z "$1" ]; then
    echo "Usage:"
    echo "run.sh start [sizeGB]"
    echo "run.sh stop"
    echo "run.sh sync"
    exit 1
fi

python3 "$SCRIPT_PATH" "$@"
