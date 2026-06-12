import uuid
from typing import Any, Dict, Optional

from ..contracts import (
    AdjudicationCaseRecord,
    AdjudicationDecisionRecord,
    FeedbackSignalRecord,
    ResolutionRecord,
)
from .base import BaseAdjudicationStrategy


class ReviewHeavyStrategy(BaseAdjudicationStrategy):
    def evaluate_case(self, case: AdjudicationCaseRecord) -> Dict[str, Any]:
        return {"recommendation": "secondary_review_suggested"}

    def process_resolution(
        self, decision: AdjudicationDecisionRecord
    ) -> ResolutionRecord:
        return ResolutionRecord(
            resolution_id=str(uuid.uuid4()),
            case_id=decision.case_id,
            resolution_family="review_heavy_resolution",
            resolution_status=(
                "applied_pending_review"
                if decision.requires_secondary_review
                else "applied"
            ),
            feedback_eligibility=True,
            memory_write_allowed=False,
            effective_scope="advisory_only",
            caveats=["Requires rigorous review before global application"],
        )

    def determine_feedback_eligibility(
        self, resolution: ResolutionRecord
    ) -> Optional[FeedbackSignalRecord]:
        return None  # In practice, generates advisory feedback
