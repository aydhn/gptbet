from sports_signal_bot.approvals.permissions import check_permission
from sports_signal_bot.approvals.contracts import OperatorIdentityRecord, RequestType

def test_operator_permissions():
    admin = OperatorIdentityRecord(operator_id="admin1", display_name="A", role="admin")
    senior = OperatorIdentityRecord(operator_id="senior1", display_name="S", role="senior_operator")
    op = OperatorIdentityRecord(operator_id="op1", display_name="O", role="operator")
    rev = OperatorIdentityRecord(operator_id="rev1", display_name="R", role="reviewer")

    assert check_permission(admin, RequestType.approve_freeze_release) is True
    assert check_permission(senior, RequestType.approve_freeze_release) is True
    assert check_permission(op, RequestType.approve_freeze_release) is False
    assert check_permission(op, RequestType.acknowledge_alarm) is True
    assert check_permission(rev, RequestType.defer_manual_review) is True
    assert check_permission(rev, RequestType.approve_high_risk_decision) is False
