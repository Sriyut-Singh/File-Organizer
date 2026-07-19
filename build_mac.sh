#!/usr/bin/env bash
# build_mac.sh — Run on macOS to produce FileOrganizer.app
# Usage: bash build_mac.sh

echo ""
echo " ============================================"
echo "   File Organizer — macOS Build Script"
echo " ============================================"
echo ""

# Check Python
if ! command -v python3 &>/dev/null; then
    echo " [ERROR] python3 not found."
    echo " Install via: brew install python-tk"
    exit 1
fi
echo " [OK] $(python3 --version)"

# Install PyInstaller
echo " Installing PyInstaller..."
pip3 install --upgrade pyinstaller --quiet

# Build
echo " Building FileOrganizer.app..."
python3 -m PyInstaller FileOrganizer.spec --clean --noconfirm

if [ $? -eq 0 ]; then
    echo ""
    echo " ✅  Build complete!"
    echo "     Output: dist/FileOrganizer.app"
    echo ""
    open dist/
else
    echo ""
    echo " ❌  Build failed. Check output above."
    exit 1
fi
