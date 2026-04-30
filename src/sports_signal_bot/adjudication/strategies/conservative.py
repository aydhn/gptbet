import uuid
from typing import Optional, Dict, Any
from .base import BaseAdjudicationStrategy
from ..contracts import (
    AdjudicationCaseRecord,
    AdjudicationDecisionRecord,
    ResolutionRecord,
    FeedbackSignalRecord
)

class ConservativeAdjudicationStrategy(BaseAdjudicationStrategy):
    def evaluate_case(self, case: AdjudicationCaseRecord) -> Dict[str, Any]:
        return {"recommendation": "require_human_confirmation"}

    def process_resolution(self, decision: AdjudicationDecisionRecord) -> ResolutionRecord:
        return ResolutionRecord(
            resolution_id=str(uuid.uuid4()),
            case_id=decision.case_id,
            resolution_family="conservative_resolution",
            resolution_status="applied",
            feedback_eligibility=False,
            memory_write_allowed=False,
            effective_scope="single_entity"
        )

    def determine_feedback_eligibility(self, resolution: ResolutionRecord) -> Optional[FeedbackSignalRecord]:
        return None
