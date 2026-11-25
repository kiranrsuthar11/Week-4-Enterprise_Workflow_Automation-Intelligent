from uuid import uuid4
def new_reference(prefix: str = "WF") -> str:
    return f"{prefix}-{uuid4().hex[:10].upper()}"
