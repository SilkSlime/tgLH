from datetime import datetime
from pathlib import Path

def get_current_timestamp() -> str:
    """Return the current timestamp as a formatted string."""
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")

def get_file_extension(file_path: str) -> str:
    """Return the file extension for the given file path."""
    return Path(file_path).suffix

def generate_unique_filename(directory: Path, stem: str, suffix: str) -> str:
    """Generate a unique filename based on the stem and suffix."""
    filename = f"{stem}_{get_current_timestamp()}{suffix}"
    while (directory / filename).exists():
        filename = f"{stem}_{get_current_timestamp()}{suffix}"
    return str(directory / filename)
