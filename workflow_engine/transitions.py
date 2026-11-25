TRANSITIONS = {"Pending": {"Approved", "Rejected"}, "Approved": set(), "Rejected": set()}
def can_transition(current: str, target: str) -> bool:
    return target in TRANSITIONS.get(current, set())
