#!/usr/bin/env bash
# ─────────────────────────────────────────────
#  File Organizer — macOS Launcher
# ─────────────────────────────────────────────

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo ""
echo " ========================================"
echo "   File Organizer — Starting..."
echo " ========================================"
echo ""

# Try python3 first, then python
PYTHON=""
if command -v python3 &>/dev/null; then
    PYTHON="python3"
elif command -v python &>/dev/null; then
    PYTHON="python"
else
    osascript -e 'display alert "Python Not Found" message "Python 3.8+ is required.\n\nInstall it from https://www.python.org/downloads/ or via Homebrew:\n  brew install python3" as critical'
    exit 1
fi

# Check tkinter availability (may be missing on some macOS Python builds)
$PYTHON -c "import tkinter" 2>/dev/null
if [ $? -ne 0 ]; then
    osascript -e 'display alert "Tkinter Missing" message "Tkinter is not available in your Python installation.\n\nInstall Python via Homebrew:\n  brew install python-tk\n\nor download from python.org which includes tkinter." as critical'
    exit 1
fi

cd "$SCRIPT_DIR"
$PYTHON file_organizer.py

if [ $? -ne 0 ]; then
    echo ""
    echo " [ERROR] App crashed. Check file_organizer.log for details."
fi
