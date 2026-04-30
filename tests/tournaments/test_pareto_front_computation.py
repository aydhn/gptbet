import pytest
from sports_signal_bot.tournaments.contracts import CandidateComparisonRecord, TournamentMetricRecord, ObjectiveDirection
from sports_signal_bot.tournaments.pareto import compute_pareto_fronts

def test_pareto_fronts():
    # c1 is strictly better than c2
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
    # c3 is mixed compared to c1
    c3 = CandidateComparisonRecord(
        comparison_id="comp3", candidate_id="c3", raw_simulation_ref="ref3",
        metrics=[
            TournamentMetricRecord(metric_name="quality", value=0.9, direction=ObjectiveDirection.MAXIMIZE),
            TournamentMetricRecord(metric_name="risk", value=0.5, direction=ObjectiveDirection.MINIMIZE)
        ]
    )

    fronts = compute_pareto_fronts([c1, c2, c3], ["quality", "risk"])

    assert len(fronts) == 2
    assert fronts[0].front_index == 1
    assert set(fronts[0].candidate_ids) == {"c1", "c3"}

    assert fronts[1].front_index == 2
    assert set(fronts[1].candidate_ids) == {"c2"}
