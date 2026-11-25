from pathlib import Path
from uuid import uuid4
def store_file(content: bytes, extension: str, directory: str = "uploads") -> str:
    folder = Path(directory); folder.mkdir(parents=True, exist_ok=True)
    name = f"{uuid4().hex}{extension.lower()}"
    (folder / name).write_bytes(content)
    return name
