import uuid
from typing import Any, Dict, Optional

from ..contracts import (
    AdjudicationCaseRecord,
    AdjudicationDecisionRecord,
    FeedbackSignalRecord,
    FeedbackStatus,
    ResolutionRecord,
)
from .base import BaseAdjudicationStrategy


class BalancedKnowledgeCaptureStrategy(BaseAdjudicationStrategy):
    def evaluate_case(self, case: AdjudicationCaseRecord) -> Dict[str, Any]:
        return {"recommendation": "default"}

    def process_resolution(
        self, decision: AdjudicationDecisionRecord
    ) -> ResolutionRecord:
        write_allowed = decision.confidence_in_resolution >= 0.8

        return ResolutionRecord(
            resolution_id=str(uuid.uuid4()),
            case_id=decision.case_id,
            resolution_family="balanced_resolution",
            resolution_status="applied",
            feedback_eligibility=True,
            memory_write_allowed=write_allowed,
            effective_scope=decision.applied_scope,
        )

    def determine_feedback_eligibility(
        self, resolution: ResolutionRecord
    ) -> Optional[FeedbackSignalRecord]:
        if not resolution.feedback_eligibility:
            return None
        return FeedbackSignalRecord(
            signal_id=str(uuid.uuid4()),
            source_resolution_id=resolution.resolution_id,
            signal_type="balanced_feedback",
            payload={"scope": resolution.effective_scope},
            status=FeedbackStatus.captured,
            confidence=0.8,
        )
