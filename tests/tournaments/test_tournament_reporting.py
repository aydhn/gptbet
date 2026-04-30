import pytest
from sports_signal_bot.tournaments.contracts import (
    TournamentCandidateRecord, CandidateComparisonRecord, TournamentGateRequirementRecord,
    TournamentEvidenceRecord, TournamentMetricRecord, ObjectiveDirection, GateBurdenBand, SafetyLane
)
from sports_signal_bot.simulation.contracts import RiskLevel
from sports_signal_bot.tournaments.reporting import generate_candidate_scorecard

def test_generate_scorecard():
    cand = TournamentCandidateRecord(
        candidate_id="c1", suggestion_id="s1", patch_id="p1", target_component_family="threshold",
        scope={}, risk_level=RiskLevel.LOW, support_strength=0.9, confidence_band="high",
        estimated_blast_radius=0.1, simulation_ref="ref1"
    )
    comp = CandidateComparisonRecord(
        comparison_id="comp1", candidate_id="c1", raw_simulation_ref="ref1", lane=SafetyLane.SAFE_SHORTLIST_LANE,
        metrics=[
            TournamentMetricRecord(metric_name="quality", value=0.8, direction=ObjectiveDirection.MAXIMIZE),
            TournamentMetricRecord(metric_name="risk", value=-0.2, direction=ObjectiveDirection.MINIMIZE) # A gain
        ]
    )
    gate = TournamentGateRequirementRecord(
        candidate_id="c1", burden_band=GateBurdenBand.LOW, required_smoke_suites=[], required_regression_suites=[],
        required_scenario_suites=[], approval_required=False, canary_mandatory=False, manual_adjudication_follow_up_needed=False
    )
    ev = TournamentEvidenceRecord(evidence_id="e1", candidate_id="c1", simulation_bundle_ref="b1", citations=[])

    scorecard = generate_candidate_scorecard(cand, comp, gate, ev)

    assert scorecard.candidate_id == "c1"
    assert len(scorecard.key_gains) == 2
    assert len(scorecard.key_regressions) == 0
