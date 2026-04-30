import pytest
from src.sports_signal_bot.tournaments.contracts import TournamentCandidateRecord
from src.sports_signal_bot.simulation.contracts import RiskLevel
from src.sports_signal_bot.tournaments.merges import propose_candidate_merge

def test_merge_detection():
    c1 = TournamentCandidateRecord(
        candidate_id="c1", suggestion_id="s1", patch_id="p1", target_component_family="threshold",
        scope={"sport": "football", "league": "EPL"}, risk_level=RiskLevel.LOW, support_strength=0.9,
        confidence_band="high", estimated_blast_radius=0.1, simulation_ref="ref1"
    )
    c2 = TournamentCandidateRecord(
        candidate_id="c2", suggestion_id="s2", patch_id="p2", target_component_family="threshold",
        scope={"sport": "football", "league": "EPL"}, risk_level=RiskLevel.LOW, support_strength=0.8,
        confidence_band="high", estimated_blast_radius=0.1, simulation_ref="ref2"
    )
    c3 = TournamentCandidateRecord(
        candidate_id="c3", suggestion_id="s3", patch_id="p3", target_component_family="threshold",
        scope={"sport": "football", "league": "LaLiga"}, risk_level=RiskLevel.LOW, support_strength=0.8,
        confidence_band="high", estimated_blast_radius=0.1, simulation_ref="ref3"
    )

    merges = propose_candidate_merge([c1, c2, c3])

    # c2 should be merged into c1
    assert "c2" in merges
    assert merges["c2"] == "c1"
    # c3 has different scope, should not be merged
    assert "c3" not in merges
