import pytest
from sports_signal_bot.candidate_promotion.contracts import CandidateReleaseRecord, CandidateLane
from sports_signal_bot.candidate_promotion.lanes import assign_lane
from sports_signal_bot.simulation.contracts import RiskLevel

def test_assign_fast_lane():
    cand = CandidateReleaseRecord(
        candidate_release_id="c1", suggestion_id="s1", patch_id="p1", tournament_ref="t1",
        target_component_family="threshold", scope={"k": "v"}, risk_level=RiskLevel.LOW, support_strength=0.9, confidence_band="high"
    )
    lane = assign_lane(cand, "low", "high")
    assert lane == CandidateLane.FAST_SAFE_CANDIDATE_LANE

def test_assign_high_risk_lane():
    cand = CandidateReleaseRecord(
        candidate_release_id="c1", suggestion_id="s1", patch_id="p1", tournament_ref="t1",
        target_component_family="threshold", scope={"k": "v"}, risk_level=RiskLevel.CRITICAL, support_strength=0.9, confidence_band="high"
    )
    lane = assign_lane(cand, "low", "high")
    assert lane == CandidateLane.HIGH_RISK_REVIEW_LANE
