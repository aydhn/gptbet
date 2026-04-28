from sports_signal_bot.approvals.requests import ApprovalRequestBuilder
from sports_signal_bot.approvals.contracts import RequestType, ApprovalScope

def test_approval_request_builder_creates_valid_request():
    req = ApprovalRequestBuilder.build_request(
        request_type=RequestType.approve_high_risk_decision,
        request_scope=ApprovalScope.single_event,
        target_entity_type="bet",
        target_entity_id="bet123",
        severity="high",
        origin_component="tests",
        requested_action="dispatch",
        rationale_summary="High risk bet needs review"
    )
    assert req.request_id.startswith("req_")
    assert req.status == "pending_review"
    assert req.requires_manual_approval is True
