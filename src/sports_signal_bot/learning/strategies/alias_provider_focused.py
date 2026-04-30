import uuid
from typing import List
from .base import BaseLearningStrategy
from ..contracts import PatternCandidateRecord, SuggestionBundleRecord
from ..suggestions import SuggestionGenerator

class AliasAndProviderFocusedStrategy(BaseLearningStrategy):
    """
    Focuses mainly on identity and provider family modifications.
    """
    def process_candidates(self, candidates: List[PatternCandidateRecord]) -> SuggestionBundleRecord:
        suggestions = []
        for c in candidates:
            if c.component_family in ["provider_trust", "alias_resolution"]:
                sug = SuggestionGenerator.generate_suggestion(c)
                suggestions.append(sug)

        return SuggestionBundleRecord(
            bundle_id=str(uuid.uuid4()),
            suggestions=suggestions,
            target_components=["provider_trust", "alias_resolution"],
            aggregate_risk="medium"
        )
