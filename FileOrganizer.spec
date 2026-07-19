# -*- mode: python ; coding: utf-8 -*-
# ─────────────────────────────────────────────────────────────────
#  FileOrganizer.spec
#  PyInstaller spec file — cross-platform, Windows-primary
#
#  WINDOWS build (run on Windows):
#    pyinstaller FileOrganizer.spec
#    → produces dist\FileOrganizer.exe
#
#  macOS build (run on macOS):
#    pyinstaller FileOrganizer.spec
#    → produces dist/FileOrganizer  (Unix binary)
#      For a proper .app bundle use build_mac.sh
#
#  Linux build (run on Linux):
#    pyinstaller FileOrganizer.spec
#    → produces dist/FileOrganizer  (ELF binary)
# ─────────────────────────────────────────────────────────────────

import sys

a = Analysis(
    ['file_organizer.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['tkinter', 'tkinter.ttk', 'tkinter.filedialog', 'tkinter.messagebox'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['numpy', 'pandas', 'matplotlib', 'PIL', 'scipy'],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='FileOrganizer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,           # Compress binary (install UPX for smaller file)
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,      # No black console window on Windows (windowed mode)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # Windows-specific: set app icon (place FileOrganizer.ico next to spec)
    # icon='FileOrganizer.ico',
)

# ── macOS .app bundle (only active when building on macOS) ───────
if sys.platform == 'darwin':
    app = BUNDLE(
        exe,
        name='FileOrganizer.app',
        icon=None,          # Replace with 'FileOrganizer.icns' if you have one
        bundle_identifier='com.fileorganizer.app',
        info_plist={
            'CFBundleName': 'File Organizer',
            'CFBundleDisplayName': 'File Organizer',
            'CFBundleVersion': '1.0.0',
            'CFBundleShortVersionString': '1.0.0',
            'NSHighResolutionCapable': True,
        },
    )
