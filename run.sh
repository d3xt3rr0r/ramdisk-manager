#!/bin/bash

BASE_DIR="$HOME/.config/ramdisk-manager"

case "$1" in
    start)
        python3 "$BASE_DIR/ramdisk.py" start "$2"
        ;;
    stop)
        python3 "$BASE_DIR/ramdisk.py" stop
        ;;
    sync)
        python3 "$BASE_DIR/ramdisk.py" sync
        ;;
    gui)
        python3 "$BASE_DIR/gui.py"
        ;;
    *)
        echo "Unknown command"
        echo "Available commands: start, stop, sync, gui"
        ;;
esac
