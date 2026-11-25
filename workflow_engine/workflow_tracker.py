from datetime import datetime, timezone
def is_overdue(created_at, deadline_days: int = 3) -> bool:
    if created_at.tzinfo is None:
        created_at = created_at.replace(tzinfo=timezone.utc)
    return (datetime.now(timezone.utc) - created_at).days > deadline_days
