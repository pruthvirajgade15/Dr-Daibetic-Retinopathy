import os
import shutil
from pathlib import Path
from typing import Optional

def save_uploaded_file(file_bytes: bytes, filename: str, destination_dir: Path) -> Path:
    destination_dir.mkdir(parents=True, exist_ok=True)
    target_path = destination_dir / filename
    with open(target_path, "wb") as f:
        f.write(file_bytes)
    return target_path

def cleanup_old_files(directory: Path, max_age_days: int = 7):
    # Optional cleanup for temporary upload caching
    pass
