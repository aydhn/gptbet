import pytest
from sports_signal_bot.learning.contracts import SupportStrength, SuggestionRiskLevel, SuggestionConfidenceBand, RecommendationMode
from sports_signal_bot.learning.patterns import PatternMiner
from sports_signal_bot.learning.risks import RiskClassifier
from sports_signal_bot.learning.confidence import ConfidenceScorer
from sports_signal_bot.learning.scopes import ScopeManager
from sports_signal_bot.learning.contracts import SuggestionScopeType, SuggestionScopeRecord, PatternSupportRecord

def test_pattern_support_strength():
    assert PatternMiner.compute_support_strength(2, 1, 0.0) == SupportStrength.insufficient
    assert PatternMiner.compute_support_strength(12, 6, 0.05) == SupportStrength.strong
    assert PatternMiner.compute_support_strength(5, 3, 0.4) == SupportStrength.weak
    assert PatternMiner.compute_support_strength(5, 3, 0.1) == SupportStrength.moderate

def test_scope_safety():
    assert ScopeManager.validate_scope_safety(SuggestionScopeType.prohibited_global_change, "global") == False
    assert ScopeManager.validate_scope_safety(SuggestionScopeType.single_entity, "narrow") == True

def test_risk_classification():
    scope = SuggestionScopeRecord(
        scope_type=SuggestionScopeType.provider_and_family_scoped,
        target_entities=["provider_x"],
        constraints={},
        is_safe=True,
        blast_radius_estimate="medium"
    )
    risk = RiskClassifier.classify_suggestion_risk(scope, "threshold", "shift_boundary")
    assert risk.risk_level in [SuggestionRiskLevel.high, SuggestionRiskLevel.medium]
    assert "critical_component_target" in risk.risk_drivers

def test_confidence_scoring():
    support = PatternSupportRecord(
        support_count=10, distinct_case_count=5, distinct_period_count=2,
        evidence_diversity_score=0.5, contradiction_burden=0.05,
        recency_weight=1.0, precedent_alignment=1.0, strength=SupportStrength.strong
    )
    conf = ConfidenceScorer.compute_suggestion_confidence(support, SuggestionRiskLevel.low, True)
    assert conf.confidence_band == SuggestionConfidenceBand.high

    mode = ConfidenceScorer.classify_recommendation_mode(conf)
    assert mode == RecommendationMode.candidate_patch
