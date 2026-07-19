#!/usr/bin/env bash
# build_linux.sh — Run on Linux to produce FileOrganizer binary
# Usage: bash build_linux.sh

echo ""
echo " ============================================"
echo "   File Organizer — Linux Build Script"
echo " ============================================"
echo ""

# Check Python
if ! command -v python3 &>/dev/null; then
    echo " [ERROR] python3 not found."
    echo " Install: sudo apt install python3 python3-tk python3-pip"
    exit 1
fi
echo " [OK] $(python3 --version)"

# Install PyInstaller
echo " Installing PyInstaller..."
pip3 install --upgrade pyinstaller --quiet

# Build
echo " Building FileOrganizer binary..."
python3 -m PyInstaller FileOrganizer.spec --clean --noconfirm

if [ $? -eq 0 ]; then
    chmod +x dist/FileOrganizer
    echo ""
    echo " ✅  Build complete!"
    echo "     Output: dist/FileOrganizer"
    echo "     Run with: ./dist/FileOrganizer"
    echo ""
else
    echo ""
    echo " ❌  Build failed. Check output above."
    exit 1
fi
