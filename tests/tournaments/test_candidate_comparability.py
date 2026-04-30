import pytest
from src.sports_signal_bot.tournaments.contracts import TournamentCandidateRecord
from src.sports_signal_bot.tournaments.candidates import block_incomparable_candidates, detect_scope_mismatch
from src.sports_signal_bot.simulation.contracts import RiskLevel

def test_comparability():
    cand1 = TournamentCandidateRecord(
        candidate_id="c1", suggestion_id="s1", patch_id="p1",
        target_component_family="threshold", scope={"sport": "football"}, risk_level=RiskLevel.LOW,
        support_strength=0.8, confidence_band="high", estimated_blast_radius=0.1, simulation_ref="ref1"
    )
    cand2 = TournamentCandidateRecord(
        candidate_id="c2", suggestion_id="s2", patch_id="p2",
        target_component_family="threshold", scope={"sport": "football", "market": "O/U"}, risk_level=RiskLevel.LOW,
        support_strength=0.8, confidence_band="high", estimated_blast_radius=0.1, simulation_ref="ref2"
    )

    assert detect_scope_mismatch(cand1, cand2) is True

    cand3 = TournamentCandidateRecord(
        candidate_id="c3", suggestion_id="s3", patch_id="p3",
        target_component_family="provider", scope={"sport": "football"}, risk_level=RiskLevel.LOW,
        support_strength=0.8, confidence_band="high", estimated_blast_radius=0.1, simulation_ref="ref3"
    )

    comp, blocked, warnings = block_incomparable_candidates([cand1, cand3])
    assert len(comp) == 1
    assert len(blocked) == 1
    assert blocked[0].candidate_id == "c3"
    assert len(warnings) == 1
