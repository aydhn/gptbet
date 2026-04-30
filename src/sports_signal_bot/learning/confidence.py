from typing import List, Dict, Any
from .contracts import (
    SuggestionConfidenceRecord,
    SuggestionConfidenceBand,
    PatternSupportRecord,
    SuggestionRiskLevel,
    RecommendationMode,
    SupportStrength
)

class ConfidenceScorer:
    @staticmethod
    def compute_suggestion_confidence(support: PatternSupportRecord, risk_level: SuggestionRiskLevel, scope_is_safe: bool) -> SuggestionConfidenceRecord:
        caveats = []
        band = SuggestionConfidenceBand.medium

        # Support based confidence
        if support.strength == SupportStrength.strong:
            band = SuggestionConfidenceBand.high
        elif support.strength == SupportStrength.weak:
            band = SuggestionConfidenceBand.low
            caveats.append("weak_support")
        elif support.strength == SupportStrength.insufficient:
            band = SuggestionConfidenceBand.unsafe_to_apply
            caveats.append("insufficient_support")

        # Risk modifiers
        if risk_level in [SuggestionRiskLevel.high, SuggestionRiskLevel.critical]:
            if band == SuggestionConfidenceBand.high:
                band = SuggestionConfidenceBand.medium
                caveats.append("downgraded_due_to_high_risk")
            elif band == SuggestionConfidenceBand.medium:
                band = SuggestionConfidenceBand.low
                caveats.append("downgraded_due_to_high_risk")

        # Scope modifiers
        if not scope_is_safe:
            band = SuggestionConfidenceBand.unsafe_to_apply
            caveats.append("unsafe_scope")

        return SuggestionConfidenceRecord(
            confidence_band=band,
            support_strength=support.strength,
            human_consistency=1.0 - support.contradiction_burden,
            contradiction_burden_category="high" if support.contradiction_burden > 0.2 else "low",
            cross_period_stability=support.distinct_period_count > 1,
            downstream_risk=risk_level,
            caveats=caveats
        )

    @staticmethod
    def classify_recommendation_mode(confidence: SuggestionConfidenceRecord) -> RecommendationMode:
        if confidence.confidence_band == SuggestionConfidenceBand.unsafe_to_apply:
            return RecommendationMode.blocked
        elif confidence.confidence_band == SuggestionConfidenceBand.exploratory_only:
            return RecommendationMode.advisory_only

        if confidence.confidence_band == SuggestionConfidenceBand.high and confidence.downstream_risk == SuggestionRiskLevel.low:
            return RecommendationMode.candidate_patch
        elif confidence.downstream_risk in [SuggestionRiskLevel.high, SuggestionRiskLevel.critical]:
            return RecommendationMode.manual_review_required

        return RecommendationMode.advisory_only

    @staticmethod
    def explain_confidence_band(confidence: SuggestionConfidenceRecord) -> str:
        return f"Confidence: {confidence.confidence_band.value}. Consistency: {confidence.human_consistency:.2f}. Caveats: {', '.join(confidence.caveats)}"

    @staticmethod
    def collect_confidence_caveats(confidence: SuggestionConfidenceRecord) -> List[str]:
        return confidence.caveats
