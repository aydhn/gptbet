import pytest
from datetime import datetime
from sports_signal_bot.tournaments.contracts import TournamentUniverseRecord, TournamentCandidateRecord
from sports_signal_bot.tournaments.universes import validate_candidate_comparability, detect_unfair_candidate_mix
from sports_signal_bot.simulation.contracts import RiskLevel

def test_universe_validation():
    universe = TournamentUniverseRecord(
        universe_id="univ_1",
        replay_window={"start": datetime.utcnow(), "end": datetime.utcnow()},
        target_sports=["football"],
        target_markets=["O/U"],
        baseline_snapshot_id="snap_1",
        release_channel_base="main",
        gate_requirements_profile="default"
    )

    cand1 = TournamentCandidateRecord(
        candidate_id="c1", suggestion_id="s1", patch_id="p1",
        target_component_family="threshold", scope={}, risk_level=RiskLevel.LOW,
        support_strength=0.8, confidence_band="high", estimated_blast_radius=0.1, simulation_ref="ref1"
    )
    cand2 = TournamentCandidateRecord(
        candidate_id="c2", suggestion_id="s2", patch_id="p2",
        target_component_family="threshold", scope={}, risk_level=RiskLevel.LOW,
        support_strength=0.8, confidence_band="high", estimated_blast_radius=0.1, simulation_ref="ref2"
    )

    is_valid, warnings = validate_candidate_comparability([cand1, cand2], universe)
    assert is_valid is True
    assert len(warnings) == 0

    cand3 = TournamentCandidateRecord(
        candidate_id="c3", suggestion_id="s3", patch_id="p3",
        target_component_family="provider", scope={}, risk_level=RiskLevel.LOW,
        support_strength=0.8, confidence_band="high", estimated_blast_radius=0.1, simulation_ref="ref3"
    )

    is_valid, warnings = validate_candidate_comparability([cand1, cand3], universe)
    assert is_valid is False
    assert len(warnings) == 1

    assert detect_unfair_candidate_mix([cand1, cand3]) is True
    assert detect_unfair_candidate_mix([cand1, cand2]) is False
