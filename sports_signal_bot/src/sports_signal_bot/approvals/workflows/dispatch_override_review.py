from sports_signal_bot.approvals.contracts import RequestType, ApprovalScope, ApprovalRequestRecord
from sports_signal_bot.approvals.requests import ApprovalRequestBuilder

def build_dispatch_override_review_request(
    dispatch_id: str,
    origin_component: str,
    rationale: str
) -> ApprovalRequestRecord:
    """Helper to construct a dispatch override request."""
    return ApprovalRequestBuilder.build_request(
        request_type=RequestType.approve_dispatch_override,
        request_scope=ApprovalScope.single_request,
        target_entity_type="dispatch",
        target_entity_id=dispatch_id,
        severity="high",
        origin_component=origin_component,
        requested_action="force_dispatch",
        rationale_summary=rationale
    )
