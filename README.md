# 🗂 File Organizer

> **Automatically sort files into folders by type — works on Windows, macOS, and Linux.**

---

## 📦 What's in this package

```
FileOrganizer/
├── file_organizer.py      ← Main app (Python source, runs on all platforms)
│
├── run_windows.bat        ← Double-click launcher for Windows (needs Python)
├── run_mac.sh             ← Launcher for macOS
├── run_linux.sh           ← Launcher for Linux
│
├── FileOrganizer.spec     ← PyInstaller config for building executables
├── build_windows.ps1      ← Build script → produces FileOrganizer.exe
├── build_mac.sh           ← Build script → produces FileOrganizer.app
└── build_linux.sh         ← Build script → produces FileOrganizer binary
```

---

## 🚀 How to Run

### ✅ Windows (Recommended — 3 options)

**Option A — Pre-built `.exe` (no Python needed)**
1. Download `FileOrganizer.exe` from the releases
2. Double-click it — done

**Option B — Run with Python**
1. Install Python 3.8+ from [python.org](https://www.python.org/downloads/)
   - ✅ Check **"Add Python to PATH"** during install
2. Double-click `run_windows.bat`

**Option C — Build the `.exe` yourself**
```powershell
# In PowerShell (right-click → Run as Administrator if needed)
.\build_windows.ps1
# Output: dist\FileOrganizer.exe
```

---

### 🍎 macOS

**Option A — Run with Python**
```bash
# Install Python if needed
brew install python-tk      # Homebrew (recommended)
# OR download from https://www.python.org/downloads/

# Then launch
bash run_mac.sh
```

**Option B — Build a native `.app`**
```bash
bash build_mac.sh
# Output: dist/FileOrganizer.app  (drag to Applications folder)
```

---

### 🐧 Linux

**Option A — Run with Python**
```bash
# Install dependencies
sudo apt install python3 python3-tk     # Ubuntu/Debian
sudo dnf install python3 python3-tkinter  # Fedora
sudo pacman -S python tk                # Arch

# Then launch
bash run_linux.sh
```

**Option B — Build a standalone binary**
```bash
bash build_linux.sh
# Output: dist/FileOrganizer  (single executable, no Python required)
chmod +x dist/FileOrganizer && ./dist/FileOrganizer
```

---

## 🖥️ How to Use the App

1. **Launch** the app using any method above
2. **Click "Browse…"** — pick the folder you want to organize
3. **Set options:**
   - ✅ *Move files* — moves files into sub-folders *(default)*
   - ☐ *Move files* unchecked — copies files, originals stay
   - ✅ *Dry Run* — preview only, nothing actually moves
4. **Click "▶ Organize Now"**
5. Watch the live log + progress bar
6. Done! ✅

> **Tip:** Always enable **Dry Run** first to preview changes safely.

---

## 📂 File Categories

| Folder | Extensions |
|---|---|
| `Images` | `.jpg` `.jpeg` `.png` `.gif` `.bmp` `.svg` `.webp` `.heic` … |
| `Videos` | `.mp4` `.mkv` `.avi` `.mov` `.wmv` `.webm` `.3gp` … |
| `Audio` | `.mp3` `.wav` `.flac` `.aac` `.ogg` `.wma` `.m4a` … |
| `Documents` | `.pdf` `.doc` `.docx` `.xls` `.xlsx` `.ppt` `.txt` `.csv` … |
| `Archives` | `.zip` `.rar` `.7z` `.tar.gz` `.cab` `.iso` … |
| `Code` | `.py` `.js` `.html` `.css` `.java` `.cpp` `.json` `.sql` … |
| `Executables` | `.exe` `.msi` `.apk` `.deb` `.rpm` `.pkg` … |
| `Fonts` | `.ttf` `.otf` `.woff` `.woff2` … |
| `3D & Design` | `.psd` `.ai` `.blend` `.obj` `.fig` `.sketch` … |
| `Data` | `.db` `.sqlite` `.parquet` `.h5` … |
| `Others` | Anything not matched above |

---

## 📁 Example

**Before:**
```
Downloads/
├── resume.pdf
├── vacation.jpg
├── song.mp3
├── setup.exe
├── notes.txt
└── project.zip
```

**After:**
```
Downloads/
├── Documents/
│   ├── resume.pdf
│   └── notes.txt
├── Images/
│   └── vacation.jpg
├── Audio/
│   └── song.mp3
├── Executables/
│   └── setup.exe
└── Archives/
    └── project.zip
```

---

## 🛡️ Safety

- **Dry Run first** — always preview before a real run
- **Name collisions** — if a file already exists at the destination, a timestamp is added automatically (e.g. `photo_20250614_102301.jpg`)
- **Sub-folders untouched** — only files directly inside the selected folder are moved; existing sub-folders are left alone
- **Log file** — every action is recorded to `file_organizer.log` in the app's directory

---

## ⚙️ Requirements

| Platform | Requirement |
|---|---|
| Windows | Python 3.8+ **or** use the pre-built `.exe` |
| macOS | Python 3.8+ with tkinter (`brew install python-tk`) |
| Linux | Python 3.8+ with tkinter (`sudo apt install python3-tk`) |

No third-party Python packages needed — uses only the standard library.

---

## 🔨 Building Executables

All build scripts use **PyInstaller** and are self-contained:

| Platform | Command | Output |
|---|---|---|
| Windows | `.\build_windows.ps1` | `dist\FileOrganizer.exe` |
| macOS | `bash build_mac.sh` | `dist/FileOrganizer.app` |
| Linux | `bash build_linux.sh` | `dist/FileOrganizer` |

> **Note:** Executables are platform-specific. A `.exe` built on Windows won't run on Linux/macOS — build on the target platform.

---

## 📝 Logs

All actions are written to `file_organizer.log`:
```
2025-06-14 10:23:01 INFO Starting organizer on: C:\Users\You\Downloads
2025-06-14 10:23:01 INFO Found 42 file(s) to process.
2025-06-14 10:23:01 INFO MOVE → [Images] vacation.jpg
2025-06-14 10:23:01 INFO MOVE → [Documents] resume.pdf
...
2025-06-14 10:23:02 INFO Organization complete!
```

---

## 📄 License

MIT License — free to use, modify, and distribute.
