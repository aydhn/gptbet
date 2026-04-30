import pytest
from sports_signal_bot.auto_promotion.engine import AutoPromotionEngine
from sports_signal_bot.auto_promotion.contracts import CandidateInputRecord, AutoDecisionType

def test_engine_run_pass():
    config = {
        "quotas": {"max_auto_progressions_per_run": 10, "max_auto_kills_per_run": 5},
        "heuristics": {"minimum_progression_score": 75.0, "low_risk_bonus": 10.0},
        "boundaries": {"stale_simulation_block_hours": 24, "minimum_evidence_for_kill": 0.8}
    }

    engine = AutoPromotionEngine(config)
    candidates = [
        # Clean
        CandidateInputRecord(
            candidate_release_id="cr-101", target_family="nba_spread", current_stage="shadow_verified",
            risk_level="low", scope_breadth="narrow", simulation_freshness_hours=2.0,
            evidence_completeness=0.9, readiness_score=0.95, gate_cleanliness=1.0, conflict_burden=0,
            dispute_count=0, repeated_holds=0
        ),
        # Stale
        CandidateInputRecord(
            candidate_release_id="cr-102", target_family="nfl_totals", current_stage="shortlisted",
            risk_level="low", scope_breadth="narrow", simulation_freshness_hours=48.0,
            evidence_completeness=0.5, readiness_score=0.3, gate_cleanliness=0.2, conflict_burden=0,
            dispute_count=0, repeated_holds=0
        )
    ]

    summary = engine.run_pass(candidates)
    assert summary.total_evaluated == 2
    assert summary.auto_progress_count == 1
    assert summary.safety_boundary_block_count == 1
