"""
File Organizer - Automatically sorts files into categorized folders
Author: Sriyut Singh
"""

import os
import shutil
import logging
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
from pathlib import Path

# ─── File Type Categories ────────────────────────────────────────────────────

FILE_CATEGORIES = {
    "Images": [
        ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp",
        ".tiff", ".tif", ".ico", ".raw", ".heic", ".heif"
    ],
    "Videos": [
        ".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm",
        ".m4v", ".mpeg", ".mpg", ".3gp", ".ts"
    ],
    "Audio": [
        ".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a",
        ".opus", ".aiff", ".mid", ".midi"
    ],
    "Documents": [
        ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
        ".txt", ".odt", ".ods", ".odp", ".rtf", ".csv", ".pages",
        ".numbers", ".key", ".epub", ".djvu"
    ],
    "Archives": [
        ".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz",
        ".tar.gz", ".tar.bz2", ".cab", ".iso", ".dmg"
    ],
    "Code": [
        ".py", ".js", ".ts", ".html", ".css", ".java", ".cpp", ".c",
        ".h", ".cs", ".php", ".rb", ".go", ".rs", ".swift", ".kt",
        ".sh", ".bat", ".ps1", ".sql", ".json", ".xml", ".yaml", ".yml",
        ".toml", ".ini", ".cfg", ".env", ".md", ".ipynb"
    ],
    "Executables": [
        ".exe", ".msi", ".apk", ".app", ".deb", ".rpm", ".pkg", ".run"
    ],
    "Fonts": [
        ".ttf", ".otf", ".woff", ".woff2", ".eot", ".fon"
    ],
    "3D & Design": [
        ".obj", ".fbx", ".stl", ".blend", ".dae", ".3ds", ".psd",
        ".ai", ".sketch", ".fig", ".xd"
    ],
    "Data": [
        ".db", ".sqlite", ".sql", ".mdb", ".accdb", ".xlsx",
        ".parquet", ".feather", ".hdf5", ".h5"
    ],
}


def get_category(file_path: Path) -> str:
    """Return the category folder name for a given file."""
    suffix = file_path.suffix.lower()
    for category, extensions in FILE_CATEGORIES.items():
        if suffix in extensions:
            return category
    return "Others"


def organize_folder(
    source_dir: str,
    move_files: bool = True,
    dry_run: bool = False,
    log_callback=None,
    progress_callback=None,
) -> dict:
    """
    Organize files in source_dir into sub-folders by type.

    Returns a summary dict with counts per category.
    """
    source = Path(source_dir)
    if not source.exists() or not source.is_dir():
        raise ValueError(f"Invalid directory: {source_dir}")

    # Collect only direct children that are files
    files = [f for f in source.iterdir() if f.is_file()]
    total = len(files)
    summary = {}
    errors = []

    def log(msg):
        if log_callback:
            log_callback(msg)
        logging.info(msg)

    log(f"{'[DRY RUN] ' if dry_run else ''}Starting organizer on: {source}")
    log(f"Found {total} file(s) to process.\n")

    for idx, file in enumerate(files, start=1):
        category = get_category(file)
        dest_folder = source / category

        if not dry_run:
            dest_folder.mkdir(exist_ok=True)

        dest_file = dest_folder / file.name

        # Handle name collisions
        if dest_file.exists() and not dry_run:
            stem = file.stem
            suffix = file.suffix
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            dest_file = dest_folder / f"{stem}_{timestamp}{suffix}"

        action = "move" if move_files else "copy"
        log(f"[{idx}/{total}] {action.upper()} → [{category}] {file.name}")

        if not dry_run:
            try:
                if move_files:
                    shutil.move(str(file), str(dest_file))
                else:
                    shutil.copy2(str(file), str(dest_file))
                summary[category] = summary.get(category, 0) + 1
            except Exception as e:
                err = f"  ✗ Error on {file.name}: {e}"
                log(err)
                errors.append(err)
        else:
            summary[category] = summary.get(category, 0) + 1

        if progress_callback:
            progress_callback(idx, total)

    log(f"\n{'─'*50}")
    log("✅ Organization complete!")
    log(f"{'─'*50}")
    for cat, count in sorted(summary.items()):
        log(f"  {cat:<20} {count} file(s)")
    if errors:
        log(f"\n⚠  {len(errors)} error(s) encountered.")
    log(f"{'─'*50}\n")

    return {"summary": summary, "errors": errors, "total": total}


# ─── GUI ─────────────────────────────────────────────────────────────────────

class FileOrganizerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("File Organizer")
        self.resizable(False, False)
        self.configure(bg="#1e1e2e")
        self._build_ui()
        self._center_window()

    # ── Layout ──────────────────────────────────────────────────────────────

    def _build_ui(self):
        ACCENT   = "#cba6f7"
        BG       = "#1e1e2e"
        SURFACE  = "#313244"
        TEXT     = "#cdd6f4"
        SUBTEXT  = "#a6adc8"
        GREEN    = "#a6e3a1"
        RED      = "#f38ba8"

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TFrame",       background=BG)
        style.configure("TLabel",       background=BG, foreground=TEXT,    font=("Segoe UI", 10))
        style.configure("Sub.TLabel",   background=BG, foreground=SUBTEXT, font=("Segoe UI", 9))
        style.configure("Head.TLabel",  background=BG, foreground=ACCENT,  font=("Segoe UI", 16, "bold"))
        style.configure("TCheckbutton", background=BG, foreground=TEXT,    font=("Segoe UI", 10))
        style.configure("Accent.TButton",
                        background=ACCENT, foreground="#11111b",
                        font=("Segoe UI", 10, "bold"), padding=8)
        style.map("Accent.TButton",
                  background=[("active", "#b4befe")],
                  relief=[("pressed", "flat")])
        style.configure("TProgressbar", troughcolor=SURFACE, background=GREEN, thickness=10)

        pad = {"padx": 20, "pady": 6}

        # Header
        ttk.Label(self, text="🗂  File Organizer", style="Head.TLabel").pack(pady=(24, 4))
        ttk.Label(self, text="Sort files into folders by type automatically.",
                  style="Sub.TLabel").pack()

        ttk.Separator(self, orient="horizontal").pack(fill="x", padx=20, pady=14)

        # Folder picker
        folder_frame = ttk.Frame(self)
        folder_frame.pack(fill="x", **pad)

        ttk.Label(folder_frame, text="Target Folder:").pack(anchor="w")

        picker_row = ttk.Frame(folder_frame)
        picker_row.pack(fill="x", pady=4)

        self.folder_var = tk.StringVar(value="No folder selected")
        folder_entry = tk.Entry(
            picker_row, textvariable=self.folder_var,
            bg=SURFACE, fg=TEXT, insertbackground=TEXT,
            relief="flat", font=("Segoe UI", 9), bd=0
        )
        folder_entry.pack(side="left", fill="x", expand=True, ipady=6, padx=(0, 8))

        browse_btn = tk.Button(
            picker_row, text="Browse…", command=self._browse,
            bg=SURFACE, fg=ACCENT, activebackground="#45475a",
            relief="flat", font=("Segoe UI", 9, "bold"), cursor="hand2", padx=10
        )
        browse_btn.pack(side="right")

        ttk.Separator(self, orient="horizontal").pack(fill="x", padx=20, pady=8)

        # Options
        opt_frame = ttk.Frame(self)
        opt_frame.pack(fill="x", **pad)
        ttk.Label(opt_frame, text="Options:").pack(anchor="w", pady=(0, 6))

        self.move_var    = tk.BooleanVar(value=True)
        self.dry_run_var = tk.BooleanVar(value=False)

        move_cb = tk.Checkbutton(
            opt_frame, text="Move files (uncheck to Copy instead)",
            variable=self.move_var,
            bg=BG, fg=TEXT, selectcolor=SURFACE,
            activebackground=BG, activeforeground=ACCENT,
            font=("Segoe UI", 10), cursor="hand2"
        )
        move_cb.pack(anchor="w")

        dry_cb = tk.Checkbutton(
            opt_frame, text="Dry Run (preview only — no files will be moved)",
            variable=self.dry_run_var,
            bg=BG, fg=TEXT, selectcolor=SURFACE,
            activebackground=BG, activeforeground=ACCENT,
            font=("Segoe UI", 10), cursor="hand2"
        )
        dry_cb.pack(anchor="w")

        ttk.Separator(self, orient="horizontal").pack(fill="x", padx=20, pady=8)

        # Progress
        prog_frame = ttk.Frame(self)
        prog_frame.pack(fill="x", **pad)

        self.progress_var = tk.DoubleVar(value=0)
        self.progress_bar = ttk.Progressbar(
            prog_frame, variable=self.progress_var,
            maximum=100, style="TProgressbar"
        )
        self.progress_bar.pack(fill="x")

        self.status_var = tk.StringVar(value="Ready.")
        ttk.Label(prog_frame, textvariable=self.status_var,
                  style="Sub.TLabel").pack(anchor="w", pady=4)

        # Log output
        log_frame = ttk.Frame(self)
        log_frame.pack(fill="both", expand=True, padx=20, pady=(0, 8))

        self.log_box = tk.Text(
            log_frame, height=12, bg=SURFACE, fg=TEXT,
            font=("Consolas", 8), relief="flat",
            state="disabled", wrap="word"
        )
        scrollbar = tk.Scrollbar(log_frame, command=self.log_box.yview)
        self.log_box.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.log_box.pack(side="left", fill="both", expand=True)

        # Buttons
        btn_row = ttk.Frame(self)
        btn_row.pack(pady=(4, 20), padx=20, fill="x")

        self.organize_btn = tk.Button(
            btn_row, text="▶  Organize Now", command=self._start,
            bg=ACCENT, fg="#11111b", activebackground="#b4befe",
            relief="flat", font=("Segoe UI", 11, "bold"),
            cursor="hand2", padx=16, pady=8
        )
        self.organize_btn.pack(side="left")

        clear_btn = tk.Button(
            btn_row, text="Clear Log", command=self._clear_log,
            bg=SURFACE, fg=SUBTEXT, activebackground="#45475a",
            relief="flat", font=("Segoe UI", 9), cursor="hand2", padx=10
        )
        clear_btn.pack(side="right")

    # ── Helpers ─────────────────────────────────────────────────────────────

    def _center_window(self):
        self.update_idletasks()
        w, h = 640, 620
        x = (self.winfo_screenwidth()  - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

    def _browse(self):
        folder = filedialog.askdirectory(title="Select Folder to Organize")
        if folder:
            self.folder_var.set(folder)

    def _log(self, msg):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", msg + "\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def _clear_log(self):
        self.log_box.configure(state="normal")
        self.log_box.delete("1.0", "end")
        self.log_box.configure(state="disabled")
        self.progress_var.set(0)
        self.status_var.set("Ready.")

    def _update_progress(self, current, total):
        pct = (current / total) * 100
        self.progress_var.set(pct)
        self.status_var.set(f"Processing {current} / {total}…")
        self.update_idletasks()

    # ── Run ─────────────────────────────────────────────────────────────────

    def _start(self):
        folder = self.folder_var.get()
        if not folder or folder == "No folder selected":
            messagebox.showwarning("No Folder", "Please select a folder first.")
            return

        self.organize_btn.configure(state="disabled")
        self.progress_var.set(0)
        self.status_var.set("Starting…")

        thread = threading.Thread(target=self._run_organizer, args=(folder,), daemon=True)
        thread.start()

    def _run_organizer(self, folder):
        try:
            result = organize_folder(
                source_dir=folder,
                move_files=self.move_var.get(),
                dry_run=self.dry_run_var.get(),
                log_callback=self._log,
                progress_callback=self._update_progress,
            )
            total   = result["total"]
            errors  = len(result["errors"])
            cats    = len(result["summary"])
            msg = f"Done! {total} file(s) sorted into {cats} categor{'y' if cats==1 else 'ies'}."
            if errors:
                msg += f" ({errors} error(s))"
            self.status_var.set(msg)
        except Exception as e:
            self._log(f"\n❌ Fatal error: {e}")
            self.status_var.set("Error occurred.")
        finally:
            self.organize_btn.configure(state="normal")
            self.progress_var.set(100)


# ─── Entry point ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    logging.basicConfig(
        filename="file_organizer.log",
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    app = FileOrganizerApp()
    app.mainloop()
