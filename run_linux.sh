#!/usr/bin/env bash
# ─────────────────────────────────────────────
#  File Organizer — Linux Launcher
# ─────────────────────────────────────────────

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo ""
echo " ========================================"
echo "   File Organizer — Starting..."
echo " ========================================"
echo ""

# Resolve python command
PYTHON=""
if command -v python3 &>/dev/null; then
    PYTHON="python3"
elif command -v python &>/dev/null; then
    PYTHON="python"
else
    echo " [ERROR] Python 3 not found."
    echo ""
    echo " Install it with:"
    echo "   Ubuntu/Debian : sudo apt install python3 python3-tk"
    echo "   Fedora        : sudo dnf install python3 python3-tkinter"
    echo "   Arch          : sudo pacman -S python tk"
    echo ""
    exit 1
fi

# Check for tkinter
$PYTHON -c "import tkinter" 2>/dev/null
if [ $? -ne 0 ]; then
    echo " [ERROR] tkinter is not installed."
    echo ""
    echo " Install it with:"
    echo "   Ubuntu/Debian : sudo apt install python3-tk"
    echo "   Fedora        : sudo dnf install python3-tkinter"
    echo "   Arch          : sudo pacman -S tk"
    echo ""
    exit 1
fi

cd "$SCRIPT_DIR"
$PYTHON file_organizer.py

if [ $? -ne 0 ]; then
    echo ""
    echo " [ERROR] App crashed. Check file_organizer.log for details."
fi
