"""Create a consistent SQLite backup using SQLite's online backup API."""
from datetime import datetime
from pathlib import Path
import sqlite3

from app.config import settings


def backup_database(destination: str | None = None) -> str:
    if not settings.database_url.startswith("sqlite:"):
        raise RuntimeError("This backup helper currently supports SQLite databases only")
    source_name = settings.database_url.removeprefix("sqlite:///")
    source = Path(source_name)
    if not source.exists():
        raise FileNotFoundError(f"Database file not found: {source}")
    target = Path(destination) if destination else Path("backups") / f"py_w4_backup_{datetime.now():%Y%m%d_%H%M%S}.db"
    target.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(source) as source_conn, sqlite3.connect(target) as target_conn:
        source_conn.backup(target_conn)
    return str(target)


if __name__ == "__main__":
    print(f"Database backup created: {backup_database()}")
