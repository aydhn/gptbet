import pytest
from sports_signal_bot.candidate_promotion.contracts import (
    CandidateReleaseRecord, CandidateState, CandidateLane
)
from sports_signal_bot.simulation.contracts import RiskLevel

def test_initial_state():
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
    assert cand.current_state == CandidateState.CANDIDATE_CREATED
    assert cand.lane is None

def test_state_transition():
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
    cand.current_state = CandidateState.PENDING_STAGE_VALIDATION
    assert cand.current_state == CandidateState.PENDING_STAGE_VALIDATION
