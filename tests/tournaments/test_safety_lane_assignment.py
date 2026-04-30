import pytest
from sports_signal_bot.tournaments.contracts import TournamentCandidateRecord, CandidateComparisonRecord, SafetyLane
from sports_signal_bot.simulation.contracts import RiskLevel
from sports_signal_bot.tournaments.lanes import classify_candidate_safety_lane

def test_lane_assignment():
    cand = TournamentCandidateRecord(
        candidate_id="c1", suggestion_id="s1", patch_id="p1",
        target_component_family="threshold", scope={}, risk_level=RiskLevel.CRITICAL,
        support_strength=0.9, confidence_band="high", estimated_blast_radius=0.5, simulation_ref="ref1"
    )
    comp = CandidateComparisonRecord(
        comparison_id="comp1", candidate_id="c1", raw_simulation_ref="ref1", metrics=[]
    )

    rules = {"high_risk_blast_threshold": 0.3}

    # Critical risk + high blast radius -> BLOCKED
    lane = classify_candidate_safety_lane(cand, comp, is_pareto_front=True, rules=rules)
    assert lane == SafetyLane.BLOCKED_LANE

    # Critical risk + low blast radius -> ADVISORY
    cand.estimated_blast_radius = 0.1
    lane = classify_candidate_safety_lane(cand, comp, is_pareto_front=True, rules=rules)
    assert lane == SafetyLane.ADVISORY_LANE

    # Low risk, front 1 -> SAFE SHORTLIST
    cand.risk_level = RiskLevel.LOW
    lane = classify_candidate_safety_lane(cand, comp, is_pareto_front=True, rules={"safe_support_threshold": 0.5})
    assert lane == SafetyLane.SAFE_SHORTLIST_LANE
