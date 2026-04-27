import uuid
from typing import List
from .contracts import (
    DispatchPayloadRecord,
    ReviewQueueRecord,
    ReviewPriorityRecord,
    ReviewReasonRecord
)

class ReviewQueueBuilder:
    def __init__(self):
        pass

    def _determine_priority(self, payload: DispatchPayloadRecord) -> ReviewPriorityRecord:
        # Placeholder logic
        if payload.signal_score > 0.8 and payload.edge > 0.05:
            return ReviewPriorityRecord(level="high", score=0.9)
        return ReviewPriorityRecord(level="medium", score=0.5)

    def _determine_reasons(self, payload: DispatchPayloadRecord) -> List[ReviewReasonRecord]:
        reasons = []
        # Placeholder logic mapping from inference payload
        if "high_disagreement" in payload.warnings:
             reasons.append(ReviewReasonRecord(code="high_disagreement", description="Models disagree significantly on probability."))
        if "stale_calibrator" in payload.warnings:
             reasons.append(ReviewReasonRecord(code="stale_calibrator", description="Calibration model is out of date."))
        if not reasons:
             reasons.append(ReviewReasonRecord(code="general_review", description="Flagged for general review by policy."))
        return reasons

    def build_from_candidate(self, payload: DispatchPayloadRecord) -> ReviewQueueRecord:
        return ReviewQueueRecord(
            review_id=f"rev_{uuid.uuid4().hex[:8]}",
            event_id=payload.event_id,
            sport=payload.sport,
            market=payload.market,
            priority=self._determine_priority(payload),
            reasons=self._determine_reasons(payload),
            signal_summary=f"Score: {payload.signal_score:.2f}, Edge: {payload.edge:.2f}"
        )
