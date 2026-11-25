from pathlib import Path
ALLOWED_EXTENSIONS = {".pdf", ".csv", ".txt", ".docx"}
def validate_file(filename: str, size: int, max_bytes: int = 10 * 1024 * 1024) -> None:
    if Path(filename).suffix.lower() not in ALLOWED_EXTENSIONS:
        raise ValueError("Unsupported file type")
    if size <= 0 or size > max_bytes:
        raise ValueError("File must be between 1 byte and 10 MB")
