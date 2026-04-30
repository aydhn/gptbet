import pytest
from sports_signal_bot.auto_promotion.contracts import CandidateInputRecord

def test_candidate_input_record_creation():
    candidate = CandidateInputRecord(
        candidate_release_id="cr-101", target_family="nba_spread", current_stage="shadow_verified",
        risk_level="low", scope_breadth="narrow", simulation_freshness_hours=2.0,
        evidence_completeness=0.9, readiness_score=0.95, gate_cleanliness=1.0, conflict_burden=0,
        dispute_count=0, repeated_holds=0
    )
    assert candidate.candidate_release_id == "cr-101"
    assert candidate.risk_level == "low"
    assert candidate.simulation_freshness_hours == 2.0
