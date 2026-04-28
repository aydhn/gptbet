import uuid
from typing import List, Optional
from sports_signal_bot.approvals.contracts import (
    ApprovalRequestRecord, RequestType, ApprovalScope
)

class ApprovalRequestBuilder:
    @staticmethod
    def build_request(
        request_type: RequestType,
        request_scope: ApprovalScope,
        target_entity_type: str,
        target_entity_id: str,
        severity: str,
        origin_component: str,
        requested_action: str,
        rationale_summary: str,
        sport: Optional[str] = None,
        market_type: Optional[str] = None,
        related_run_ids: Optional[List[str]] = None,
        related_event_ids: Optional[List[str]] = None,
        warnings: Optional[List[str]] = None
    ) -> ApprovalRequestRecord:

        return ApprovalRequestRecord(
            request_id=f"req_{uuid.uuid4().hex[:8]}",
            request_type=request_type,
            request_scope=request_scope,
            target_entity_type=target_entity_type,
            target_entity_id=target_entity_id,
            sport=sport,
            market_type=market_type,
            severity=severity,
            origin_component=origin_component,
            requested_action=requested_action,
            rationale_summary=rationale_summary,
            related_run_ids=related_run_ids or [],
            related_event_ids=related_event_ids or [],
            warnings=warnings or []
        )
