import pytest
from sports_signal_bot.candidate_promotion.stages import build_candidate_validation_plan
from sports_signal_bot.candidate_promotion.contracts import CandidateReleaseRecord
from sports_signal_bot.simulation.contracts import RiskLevel

def test_build_plan_low_risk():
    cand = CandidateReleaseRecord(
        candidate_release_id="c1",
        suggestion_id="s1",
        patch_id="p1",
        tournament_ref="t1",
        target_component_family="threshold",
        scope={},
        risk_level=RiskLevel.LOW,
        support_strength=0.9,
        confidence_band="high"
    )
    plan = build_candidate_validation_plan(cand)
    assert "review_readiness_validation" not in plan
    assert "integrity_validation" in plan

def test_build_plan_critical_risk():
    cand = CandidateReleaseRecord(
        candidate_release_id="c1",
        suggestion_id="s1",
        patch_id="p1",
        tournament_ref="t1",
        target_component_family="threshold",
        scope={},
        risk_level=RiskLevel.CRITICAL,
        support_strength=0.9,
        confidence_band="high"
    )
    plan = build_candidate_validation_plan(cand)
    assert "review_readiness_validation" in plan
