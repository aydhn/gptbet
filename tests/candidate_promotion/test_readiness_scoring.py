import pytest
from sports_signal_bot.candidate_promotion.contracts import (
    CandidateReleaseRecord, CandidateValidationStageRecord, CandidateReadinessBand
)
from sports_signal_bot.candidate_promotion.readiness import compute_candidate_readiness
from sports_signal_bot.simulation.contracts import RiskLevel

def test_compute_readiness_all_pass_low_risk():
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
    stages = [
        CandidateValidationStageRecord(validation_id="v1", candidate_id="c1", stage_id="safety_validation", passed=True)
    ]
    readiness = compute_candidate_readiness(cand, stages, has_approvals=False)
    assert readiness.readiness_band == CandidateReadinessBand.RELEASE_CANDIDATE_READY

def test_compute_readiness_fail_safety():
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
    stages = [
        CandidateValidationStageRecord(validation_id="v1", candidate_id="c1", stage_id="safety_validation", passed=False)
    ]
    readiness = compute_candidate_readiness(cand, stages, has_approvals=False)
    assert readiness.readiness_band == CandidateReadinessBand.BLOCKED_NOT_READY
