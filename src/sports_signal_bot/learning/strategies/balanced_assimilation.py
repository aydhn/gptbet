import uuid
from typing import List
from .base import BaseLearningStrategy
from ..contracts import PatternCandidateRecord, SuggestionBundleRecord, SuggestionRiskLevel
from ..suggestions import SuggestionGenerator

class BalancedAssimilationStrategy(BaseLearningStrategy):
    """
    Default strategy. Moderate support can produce candidate patches.
    Strong risk and scope guards.
    """
    def process_candidates(self, candidates: List[PatternCandidateRecord]) -> SuggestionBundleRecord:
        suggestions = []
        highest_risk = SuggestionRiskLevel.low

        for c in candidates:
            sug = SuggestionGenerator.generate_suggestion(c)
            suggestions.append(sug)

            # Update aggregate risk
            if sug.estimated_risk.risk_level == SuggestionRiskLevel.critical:
                highest_risk = SuggestionRiskLevel.critical
            elif sug.estimated_risk.risk_level == SuggestionRiskLevel.high and highest_risk != SuggestionRiskLevel.critical:
                highest_risk = SuggestionRiskLevel.high
            elif sug.estimated_risk.risk_level == SuggestionRiskLevel.medium and highest_risk == SuggestionRiskLevel.low:
                highest_risk = SuggestionRiskLevel.medium

        return SuggestionBundleRecord(
            bundle_id=str(uuid.uuid4()),
            suggestions=suggestions,
            target_components=list(set(s.target_component_family for s in suggestions)),
            aggregate_risk=highest_risk
        )
