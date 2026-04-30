import pytest
from src.sports_signal_bot.tournaments.contracts import CandidateComparisonRecord, TournamentMetricRecord, ObjectiveDirection
from src.sports_signal_bot.tournaments.pareto import dominates

def test_dominates():
    c1 = CandidateComparisonRecord(
        comparison_id="comp1", candidate_id="c1", raw_simulation_ref="ref1",
        metrics=[
            TournamentMetricRecord(metric_name="quality", value=0.8, direction=ObjectiveDirection.MAXIMIZE),
            TournamentMetricRecord(metric_name="risk", value=0.1, direction=ObjectiveDirection.MINIMIZE)
        ]
    )
    c2 = CandidateComparisonRecord(
        comparison_id="comp2", candidate_id="c2", raw_simulation_ref="ref2",
        metrics=[
            TournamentMetricRecord(metric_name="quality", value=0.5, direction=ObjectiveDirection.MAXIMIZE),
            TournamentMetricRecord(metric_name="risk", value=0.3, direction=ObjectiveDirection.MINIMIZE)
        ]
    )

    is_dom, metrics = dominates(c1, c2, ["quality", "risk"])
    assert is_dom is True
    assert "quality" in metrics
    assert "risk" in metrics

    is_dom, metrics = dominates(c2, c1, ["quality", "risk"])
    assert is_dom is False
