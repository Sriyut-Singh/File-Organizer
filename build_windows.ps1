# build_windows.ps1
# Run this on a Windows machine to produce FileOrganizer.exe
# Usage:  .\build_windows.ps1

Write-Host ""
Write-Host " ============================================" -ForegroundColor Cyan
Write-Host "   File Organizer — Windows Build Script" -ForegroundColor Cyan
Write-Host " ============================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
try {
    $pyver = python --version 2>&1
    Write-Host " [OK] Found: $pyver" -ForegroundColor Green
} catch {
    Write-Host " [ERROR] Python not found. Install from https://python.org" -ForegroundColor Red
    exit 1
}

# Install / upgrade PyInstaller
Write-Host ""
Write-Host " Installing PyInstaller..." -ForegroundColor Yellow
pip install --upgrade pyinstaller | Out-Null

# Build
Write-Host " Building FileOrganizer.exe..." -ForegroundColor Yellow
pyinstaller FileOrganizer.spec --clean --noconfirm

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host " ✅  Build complete!" -ForegroundColor Green
    Write-Host "     Output: dist\FileOrganizer.exe" -ForegroundColor Green
    Write-Host ""
    # Open dist folder
    Start-Process explorer.exe "dist"
} else {
    Write-Host ""
    Write-Host " ❌  Build failed. Check output above." -ForegroundColor Red
    exit 1
}
