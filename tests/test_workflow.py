from workflow_engine.transitions import can_transition

def test_pending_can_be_approved():
    assert can_transition("Pending", "Approved")

def test_pending_can_be_rejected():
    assert can_transition("Pending", "Rejected")

def test_approved_is_terminal():
    assert not can_transition("Approved", "Rejected")

def test_rejected_is_terminal():
    assert not can_transition("Rejected", "Approved")
