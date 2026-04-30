import pytest
from src.sports_signal_bot.tournaments.contracts import TournamentCandidateRecord, GateBurdenBand
from src.sports_signal_bot.simulation.contracts import RiskLevel
from src.sports_signal_bot.tournaments.gate_burden import compute_gate_burden

def test_gate_burden():
    c1 = TournamentCandidateRecord(
        candidate_id="c1", suggestion_id="s1", patch_id="p1", target_component_family="threshold",
        scope={}, risk_level=RiskLevel.LOW, support_strength=0.9, confidence_band="high",
        estimated_blast_radius=0.1, simulation_ref="ref1"
    )

    # Low risk, low blast radius
    gate = compute_gate_burden(c1, {})
    assert gate.burden_band == GateBurdenBand.LOW
    assert gate.approval_required is False
    assert gate.canary_mandatory is False

    # Critical risk
    c1.risk_level = RiskLevel.CRITICAL
    gate = compute_gate_burden(c1, {})
    assert gate.burden_band == GateBurdenBand.VERY_HIGH
    assert gate.approval_required is True
    assert gate.canary_mandatory is True
    assert gate.manual_adjudication_follow_up_needed is True

    # Low risk, but high blast radius
    c1.risk_level = RiskLevel.LOW
    c1.estimated_blast_radius = 0.8
    gate = compute_gate_burden(c1, {})
    assert gate.burden_band == GateBurdenBand.HIGH
    assert gate.canary_mandatory is True
