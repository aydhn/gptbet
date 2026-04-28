from sports_signal_bot.approvals.contracts import RequestType, ApprovalScope, ApprovalRequestRecord
from sports_signal_bot.approvals.requests import ApprovalRequestBuilder

def build_decision_review_request(
    decision_id: str,
    origin_component: str,
    rationale: str,
    sport: str = None,
    market_type: str = None,
    severity: str = "high"
) -> ApprovalRequestRecord:
    """Helper to construct a decision review request."""
    return ApprovalRequestBuilder.build_request(
        request_type=RequestType.approve_high_risk_decision,
        request_scope=ApprovalScope.single_event,
        target_entity_type="decision",
        target_entity_id=decision_id,
        severity=severity,
        origin_component=origin_component,
        requested_action="approve_dispatch",
        rationale_summary=rationale,
        sport=sport,
        market_type=market_type
    )
