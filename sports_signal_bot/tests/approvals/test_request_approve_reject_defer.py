from sports_signal_bot.approvals.decisions import ApprovalDecisionApplier
from sports_signal_bot.approvals.requests import ApprovalRequestBuilder
from sports_signal_bot.approvals.contracts import RequestType, ApprovalScope, RequestStatus

def test_approve_reject_defer_flow():
    req = ApprovalRequestBuilder.build_request(
        request_type=RequestType.approve_high_risk_decision,
        request_scope=ApprovalScope.single_event,
        target_entity_type="bet",
        target_entity_id="bet123",
        severity="high",
        origin_component="tests",
        requested_action="dispatch",
        rationale_summary="High risk bet"
    )

    dec1 = ApprovalDecisionApplier.defer(req, "op1", "Need more info")
    assert req.status == RequestStatus.deferred
    assert dec1.decision_type == "defer"
    assert dec1.execution_authorized is False

    dec2 = ApprovalDecisionApplier.approve(req, "senior1", "Looks good")
    assert req.status == RequestStatus.approved
    assert dec2.decision_type == "approve"
    assert dec2.execution_authorized is True

    dec3 = ApprovalDecisionApplier.reject(req, "admin1", "Too risky")
    assert req.status == RequestStatus.rejected
    assert dec3.decision_type == "reject"
    assert dec3.execution_authorized is False
