import uuid
from typing import List
from .base import BaseLearningStrategy
from ..contracts import PatternCandidateRecord, SuggestionBundleRecord, RecommendationMode
from ..suggestions import SuggestionGenerator

class AdvisoryFirstStrategy(BaseLearningStrategy):
    """
    Generates many suggestions but keeps them strictly advisory. Good for discovery.
    """
    def process_candidates(self, candidates: List[PatternCandidateRecord]) -> SuggestionBundleRecord:
        suggestions = []
        for c in candidates:
            sug = SuggestionGenerator.generate_suggestion(c)
            # Downgrade anything that isn't blocked to advisory
            if sug.recommendation_mode != RecommendationMode.blocked:
                 sug.recommendation_mode = RecommendationMode.advisory_only
            suggestions.append(sug)

        return SuggestionBundleRecord(
            bundle_id=str(uuid.uuid4()),
            suggestions=suggestions,
            target_components=list(set(s.target_component_family for s in suggestions)),
            aggregate_risk="low"
        )
