from sports_signal_bot.approvals.contracts import RequestType, ApprovalScope, ApprovalRequestRecord
from sports_signal_bot.approvals.requests import ApprovalRequestBuilder

def build_anomaly_ack_request(
    anomaly_id: str,
    origin_component: str,
    rationale: str
) -> ApprovalRequestRecord:
    """Helper to construct an anomaly ack request."""
    return ApprovalRequestBuilder.build_request(
        request_type=RequestType.acknowledge_alarm,
        request_scope=ApprovalScope.single_request,
        target_entity_type="anomaly",
        target_entity_id=anomaly_id,
        severity="medium",
        origin_component=origin_component,
        requested_action="acknowledge",
        rationale_summary=rationale
    )
