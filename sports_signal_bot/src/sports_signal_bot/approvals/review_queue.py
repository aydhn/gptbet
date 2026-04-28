import uuid
from typing import List
from sports_signal_bot.approvals.contracts import (
    ReviewItemRecord, ReviewItemType, ApprovalRequestRecord
)

class ReviewQueueBuilder:
    @staticmethod
    def create_item_from_request(request: ApprovalRequestRecord, priority: str = "medium") -> ReviewItemRecord:

        category_map = {
            "approve_high_risk_decision": ReviewItemType.decision_review_item,
            "approve_refresh_plan": ReviewItemType.refresh_review_item,
            "approve_freeze_release": ReviewItemType.freeze_release_item,
            "approve_dispatch_override": ReviewItemType.dispatch_review_item,
            "create_manual_override": ReviewItemType.manual_override_item
        }
        category = category_map.get(request.request_type, ReviewItemType.anomaly_review_item)

        return ReviewItemRecord(
            review_id=f"rev_{uuid.uuid4().hex[:8]}",
            priority=priority,
            category=category,
            title=f"Review required for {request.target_entity_type} {request.target_entity_id}",
            summary=request.rationale_summary,
            request_ref=request.request_id,
            risk_level=request.severity
        )

def assign_review_priority(severity: str, request_type: str) -> str:
    """Assign a priority (critical, high, medium, low)."""
    if severity == "critical" or request_type == "approve_freeze_release":
        return "critical"
    elif severity == "high" or request_type == "approve_refresh_plan":
        return "high"
    elif severity == "low":
        return "low"
    return "medium"

def sort_review_queue(items: List[ReviewItemRecord]) -> List[ReviewItemRecord]:
    """Sort queue by priority then creation time."""
    priority_map = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    return sorted(items, key=lambda x: (priority_map.get(x.priority, 99), x.created_at))
