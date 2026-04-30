import uuid
from typing import List
from .base import BaseLearningStrategy
from ..contracts import PatternCandidateRecord, SuggestionBundleRecord
from ..suggestions import SuggestionGenerator

class PolicyBoundaryFocusedStrategy(BaseLearningStrategy):
    """
    Focuses on false no_bet, false block, and borderline candidates.
    """
    def process_candidates(self, candidates: List[PatternCandidateRecord]) -> SuggestionBundleRecord:
        suggestions = []
        for c in candidates:
            if c.component_family in ["policy", "threshold"]:
                sug = SuggestionGenerator.generate_suggestion(c)
                suggestions.append(sug)

        return SuggestionBundleRecord(
            bundle_id=str(uuid.uuid4()),
            suggestions=suggestions,
            target_components=["policy", "threshold"],
            aggregate_risk="high"
        )
