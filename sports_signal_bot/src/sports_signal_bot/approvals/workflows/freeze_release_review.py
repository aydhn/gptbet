from sports_signal_bot.approvals.contracts import RequestType, ApprovalScope, ApprovalRequestRecord
from sports_signal_bot.approvals.requests import ApprovalRequestBuilder

def build_freeze_release_review_request(
    freeze_id: str,
    origin_component: str,
    rationale: str
) -> ApprovalRequestRecord:
    """Helper to construct a freeze release review request."""
    return ApprovalRequestBuilder.build_request(
        request_type=RequestType.approve_freeze_release,
        request_scope=ApprovalScope.freeze_release_once,
        target_entity_type="freeze",
        target_entity_id=freeze_id,
        severity="critical",
        origin_component=origin_component,
        requested_action="release_freeze",
        rationale_summary=rationale
    )
