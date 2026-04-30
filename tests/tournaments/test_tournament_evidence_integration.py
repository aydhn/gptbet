import pytest
from sports_signal_bot.tournaments.contracts import CandidateComparisonRecord, TournamentMetricRecord, ObjectiveDirection
from sports_signal_bot.tournaments.evidences import attach_evidence_to_tournament_candidate, build_tournament_claims, explain_dominance_with_citations

def test_evidence_integration():
    ev = attach_evidence_to_tournament_candidate("c1", "sim_run_123", ["cit_1", "cit_2"])
    assert ev.candidate_id == "c1"
    assert ev.simulation_bundle_ref == "bundle_for_run_sim_run_123"
    assert len(ev.citations) == 2

    comp = CandidateComparisonRecord(
        comparison_id="comp1", candidate_id="c1", raw_simulation_ref="ref1",
        metrics=[
            TournamentMetricRecord(metric_name="quality", value=0.8, direction=ObjectiveDirection.MAXIMIZE)
        ]
    )

    claims = build_tournament_claims(comp)
    assert len(claims) == 1
    assert "quality" in claims[0]

    explanation = explain_dominance_with_citations("c1", "c2", ["quality"], {"c1": ev})
    assert "c1 dominates c2" in explanation
    assert "bundle_for_run_sim_run_123" in explanation
