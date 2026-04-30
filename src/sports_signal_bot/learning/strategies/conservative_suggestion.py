import uuid
from typing import List
from .base import BaseLearningStrategy
from ..contracts import PatternCandidateRecord, SuggestionBundleRecord, RecommendationMode
from ..suggestions import SuggestionGenerator

class ConservativeSuggestionStrategy(BaseLearningStrategy):
    """
    Looks for high support and narrow scope. Leaves most things advisory.
    """
    def process_candidates(self, candidates: List[PatternCandidateRecord]) -> SuggestionBundleRecord:
        suggestions = []
        for c in candidates:
            sug = SuggestionGenerator.generate_suggestion(c)
            # Force most things to advisory if they aren't already
            if sug.recommendation_mode != RecommendationMode.blocked:
                 sug.recommendation_mode = RecommendationMode.advisory_only
            suggestions.append(sug)

        return SuggestionBundleRecord(
            bundle_id=str(uuid.uuid4()),
            suggestions=suggestions,
            target_components=["all_conservative"],
            aggregate_risk="low"
        )
