#!/usr/bin/env python3
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import json

# ----------------------
# CONFIG
# ----------------------
INPUT_DIR = Path("documents").resolve()
OUTPUT_DIR = Path("ocr_output").resolve()

INPUT_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# ----------------------
# PROCESS PDF
# ----------------------
def process_pdf(pdf_path: Path):
    rel_path = pdf_path.resolve().relative_to(INPUT_DIR)
    output_folder = OUTPUT_DIR / rel_path.parent / pdf_path.stem
    output_folder.mkdir(parents=True, exist_ok=True)

    status_file = output_folder / "status.json"

    print(f"Processing PDF: {pdf_path} -> {output_folder}")

    # Initially mark as not complete
    with open(status_file, "w", encoding="utf-8") as f:
        json.dump({"complete_docling": 1}, f)

    try:
        # Run docling
        subprocess.run(
            ["docling", str(pdf_path), "--output", str(output_folder)],
            check=True
        )
        # Mark as complete
        with open(status_file, "w", encoding="utf-8") as f:
            json.dump({"complete_docling": 0}, f)
        print(f"Finished: {pdf_path} -> complete_docling: 0")
    except subprocess.CalledProcessError as e:
        print(f"Error processing {pdf_path}: {e}")
        # Keep complete_docling = 1
        print(f"Finished: {pdf_path} -> complete_docling: 1")

# ----------------------
# WATCHDOG HANDLER
# ----------------------
class PDFHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        path = Path(event.src_path)
        if path.suffix.lower() == ".pdf":
            process_pdf(path)

    def on_moved(self, event):
        if event.is_directory:
            return
        path = Path(event.dest_path)
        if path.suffix.lower() == ".pdf":
            process_pdf(path)

# ----------------------
# SCAN EXISTING PDFs
# ----------------------
def scan_existing():
    print("Scanning existing PDFs...")
    for pdf in INPUT_DIR.rglob("*.pdf"):
        process_pdf(pdf)

# ----------------------
# START WATCHING
# ----------------------
def start_watching():
    observer = Observer()
    handler = PDFHandler()
    observer.schedule(handler, str(INPUT_DIR), recursive=True)
    observer.start()
    print(f"Watching folder: {INPUT_DIR}")
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# ----------------------
# MAIN
# ----------------------
if __name__ == "__main__":
    scan_existing()
    start_watching()