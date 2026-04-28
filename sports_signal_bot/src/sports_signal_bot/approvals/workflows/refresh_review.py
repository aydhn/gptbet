from sports_signal_bot.approvals.contracts import RequestType, ApprovalScope, ApprovalRequestRecord
from sports_signal_bot.approvals.requests import ApprovalRequestBuilder

def build_refresh_review_request(
    refresh_plan_id: str,
    origin_component: str,
    rationale: str,
    severity: str = "high"
) -> ApprovalRequestRecord:
    """Helper to construct a refresh plan review request."""
    return ApprovalRequestBuilder.build_request(
        request_type=RequestType.approve_refresh_plan,
        request_scope=ApprovalScope.single_run,
        target_entity_type="refresh_plan",
        target_entity_id=refresh_plan_id,
        severity=severity,
        origin_component=origin_component,
        requested_action="execute_refresh",
        rationale_summary=rationale
    )
