import pytest
from sports_signal_bot.candidate_promotion.stages import run_candidate_stage_validation
from sports_signal_bot.candidate_promotion.contracts import CandidateReleaseRecord
from sports_signal_bot.simulation.contracts import RiskLevel

def test_safety_stage_critical_fails():
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
    res = run_candidate_stage_validation(cand, "safety_validation")
    assert res.passed is False

def test_safety_stage_low_passes():
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
    res = run_candidate_stage_validation(cand, "safety_validation")
    assert res.passed is True
