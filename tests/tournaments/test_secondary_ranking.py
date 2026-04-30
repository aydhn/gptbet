import pytest
from sports_signal_bot.tournaments.contracts import TournamentCandidateRecord, CandidateComparisonRecord, ParetoFrontRecord
from sports_signal_bot.simulation.contracts import RiskLevel
from sports_signal_bot.tournaments.ranking import rank_within_front

def test_secondary_ranking():
    c1 = TournamentCandidateRecord(
        candidate_id="c1", suggestion_id="s1", patch_id="p1", target_component_family="threshold",
        scope={}, risk_level=RiskLevel.LOW, support_strength=0.9, confidence_band="high",
        estimated_blast_radius=0.1, simulation_ref="ref1"
    )
    c2 = TournamentCandidateRecord(
        candidate_id="c2", suggestion_id="s2", patch_id="p2", target_component_family="threshold",
        scope={}, risk_level=RiskLevel.MEDIUM, support_strength=0.8, confidence_band="medium",
        estimated_blast_radius=0.2, simulation_ref="ref2"
    )

    comp1 = CandidateComparisonRecord(comparison_id="comp1", candidate_id="c1", raw_simulation_ref="ref1", metrics=[])
    comp2 = CandidateComparisonRecord(comparison_id="comp2", candidate_id="c2", raw_simulation_ref="ref2", metrics=[])

    front = ParetoFrontRecord(front_index=1, candidate_ids=["c1", "c2"], relations=[])

    candidates = {"c1": c1, "c2": c2}
    comparisons = {"c1": comp1, "c2": comp2}

    rankings = rank_within_front(front, candidates, comparisons, {"blast_radius_penalty_weight": 10.0, "support_weight": 5.0})

    assert len(rankings) == 2
    assert rankings[0].candidate_id == "c1" # C1 is lower risk and higher support
    assert rankings[1].candidate_id == "c2"
