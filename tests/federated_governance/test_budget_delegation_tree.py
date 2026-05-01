from sports_signal_bot.federated_governance.budgets import allocate_local_plane_budget, reserve_budget_from_parent, transfer_budget_if_allowed, detect_budget_violation

def test_allocate_and_reserve_budget():
    b1 = allocate_local_plane_budget("p1", "risk", 100.0)
    assert b1.total_amount == 100.0

    success = reserve_budget_from_parent(b1, 50.0)
    assert success is True
    assert b1.reserved_amount == 50.0

    success_fail = reserve_budget_from_parent(b1, 60.0)
    assert success_fail is False

def test_transfer_budget():
    b1 = allocate_local_plane_budget("p1", "risk", 100.0)
    b2 = allocate_local_plane_budget("p2", "risk", 0.0)

    trx = transfer_budget_if_allowed(b1, b2, 40.0)
    assert trx is not None
    assert b1.total_amount == 60.0
    assert b2.total_amount == 40.0

def test_detect_budget_violation():
    b1 = allocate_local_plane_budget("p1", "risk", 50.0)
    b1.used_amount = 40.0

    viol = detect_budget_violation(b1, 20.0)
    assert viol is not None
    assert viol.attempted_amount == 20.0
