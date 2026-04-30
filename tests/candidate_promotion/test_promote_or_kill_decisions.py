import pytest
from sports_signal_bot.candidate_promotion.contracts import (
    CandidateReleaseRecord, CandidateReadinessRecord, CandidateReadinessBand, CandidateLane, FinalDecisionAction
)
from sports_signal_bot.candidate_promotion.decisions import build_promote_or_kill_decision
from sports_signal_bot.simulation.contracts import RiskLevel

def test_build_decision_promote():
    cand = CandidateReleaseRecord(
        candidate_release_id="c1", suggestion_id="s1", patch_id="p1", tournament_ref="t1",
        target_component_family="threshold", scope={}, risk_level=RiskLevel.LOW, support_strength=0.9, confidence_band="high"
    )
    readiness = CandidateReadinessRecord(
        readiness_id="r1", candidate_id="c1", readiness_band=CandidateReadinessBand.RELEASE_CANDIDATE_READY, missing_requirements=[]
    )
    action, rat = build_promote_or_kill_decision(cand, readiness, CandidateLane.STANDARD_CANDIDATE_LANE)
    assert action == FinalDecisionAction.PROMOTE_CANDIDATE_LANE

def test_build_decision_kill_safety():
    cand = CandidateReleaseRecord(
        candidate_release_id="c1", suggestion_id="s1", patch_id="p1", tournament_ref="t1",
        target_component_family="threshold", scope={}, risk_level=RiskLevel.CRITICAL, support_strength=0.9, confidence_band="high"
    )
    readiness = CandidateReadinessRecord(
        readiness_id="r1", candidate_id="c1", readiness_band=CandidateReadinessBand.BLOCKED_NOT_READY, missing_requirements=["safety_validation"]
    )
    action, rat = build_promote_or_kill_decision(cand, readiness, CandidateLane.STANDARD_CANDIDATE_LANE)
    assert action == FinalDecisionAction.KILL_CANDIDATE
