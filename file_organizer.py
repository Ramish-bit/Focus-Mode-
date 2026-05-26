import os, shutil, sys
from pathlib import Path
from datetime import datetime

CATEGORIES = {
    "PDFs":       [".pdf"],
    "Images":     [".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".bmp", ".ico", ".tiff"],
    "Code":       [".py", ".js", ".ts", ".html", ".css", ".cpp", ".c", ".java", ".rs", ".go",
                   ".rb", ".php", ".sh", ".bat", ".json", ".xml", ".yaml", ".yml", ".toml"],
    "Installers": [".exe", ".dmg", ".pkg", ".deb", ".rpm", ".msi", ".appimage"],
    "Documents":  [".docx", ".doc", ".xlsx", ".xls", ".pptx", ".ppt", ".txt", ".md", ".csv", ".rtf"],
    "Archives":   [".zip", ".rar", ".tar", ".gz", ".7z", ".bz2", ".xz"],
    "Videos":     [".mp4", ".mkv", ".mov", ".avi", ".webm", ".flv"],
    "Audio":      [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"],
}

def get_category(ext):
    for cat, exts in CATEGORIES.items():
        if ext.lower() in exts:
            return cat
    return "Misc"

def organize(folder_path, dry_run=False):
    folder = Path(folder_path)
    if not folder.exists():
        print(f"[!] Path not found: {folder}")
        sys.exit(1)

    moved, skipped, errors = 0, 0, 0

    print(f"  Scanning {folder}...\n")

    for item in sorted(folder.iterdir()):
        if item.is_dir():
            skipped += 1
            continue

        category  = get_category(item.suffix)
        dest_dir  = folder / category
        dest_file = dest_dir / item.name

        # Avoid overwriting — append timestamp if name collision
        if dest_file.exists():
            ts        = datetime.now().strftime("%Y%m%d_%H%M%S")
            dest_file = dest_dir / f"{item.stem}_{ts}{item.suffix}"

        if not dry_run:
            dest_dir.mkdir(exist_ok=True)
            try:
                shutil.move(str(item), str(dest_file))
                print(f"  [✓] {item.name:<35} →  {category}/")
                moved += 1
            except Exception as e:
                print(f"  [✗] {item.name:<35}    ERROR: {e}")
                errors += 1
        else:
            print(f"  [dry] {item.name:<33} →  {category}/")
            moved += 1

    print(f"\n{'='*50}")
    print(f"  {'DRY RUN — no files were moved' if dry_run else 'Organisation complete'}")
    print(f"  Organised : {moved} files")
    print(f"  Skipped   : {skipped} folders")
    print(f"  Errors    : {errors}")
    print(f"{'='*50}\n")

if __name__ == "__main__":
    # Usage:
    #   python file_organizer.py                    (uses ~/Downloads)
    #   python file_organizer.py /path/to/folder
    #   python file_organizer.py /path/to/folder --dry-run
    path    = sys.argv[1] if len(sys.argv) > 1 else str(Path.home() / "Downloads")
    dry_run = "--dry-run" in sys.argv

    print(f"\n{'='*50}")
    print(f"  📁 FILE ORGANIZER")
    print(f"  Folder : {path}")
    print(f"  Mode   : {'DRY RUN (no changes)' if dry_run else 'LIVE'}")
    print(f"{'='*50}\n")

    organize(path, dry_run)
