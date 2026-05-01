from sports_signal_bot.federated_governance.contracts import ControlPlaneRecord, PlanePrecedence, PlaneHealthBand, PlaneBudgetRecord
from sports_signal_bot.federated_governance.planes import validate_parent_child_governance
from sports_signal_bot.federated_governance.budgets import detect_budget_violation

def test_federated_admission():
    # Mocking a basic federated admission control flow
    global_plane = ControlPlaneRecord(plane_id="global", plane_name="Global", plane_family="global", precedence=PlanePrecedence.GLOBAL_GOVERNANCE)
    family_plane = ControlPlaneRecord(plane_id="family", plane_name="Family", plane_family="family", precedence=PlanePrecedence.FAMILY_DOMAIN, parent_plane_id="global")

    assert validate_parent_child_governance(global_plane, family_plane) is True

    family_budget = PlaneBudgetRecord(budget_id="b1", plane_id="family", budget_type="risk", total_amount=10.0, used_amount=9.0)

    viol = detect_budget_violation(family_budget, 2.0)
    assert viol is not None  # Admission blocked due to budget
