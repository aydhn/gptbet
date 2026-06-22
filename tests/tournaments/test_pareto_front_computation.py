from sports_signal_bot.tournaments.contracts import (CandidateComparisonRecord,
                                                     ObjectiveDirection,
                                                     TournamentMetricRecord)
from sports_signal_bot.tournaments.pareto import compute_pareto_fronts


def test_pareto_fronts():
    # c1 is strictly better than c2
    c1 = CandidateComparisonRecord(
        comparison_id="comp1",
        candidate_id="c1",
        raw_simulation_ref="ref1",
        metrics=[
            TournamentMetricRecord(
                metric_name="quality",
                value=0.8,
                direction=ObjectiveDirection.MAXIMIZE,
            ),
            TournamentMetricRecord(
                metric_name="risk",
                value=0.1,
                direction=ObjectiveDirection.MINIMIZE,
            ),
        ],
    )
    c2 = CandidateComparisonRecord(
        comparison_id="comp2",
        candidate_id="c2",
        raw_simulation_ref="ref2",
        metrics=[
            TournamentMetricRecord(
                metric_name="quality",
                value=0.5,
                direction=ObjectiveDirection.MAXIMIZE,
            ),
            TournamentMetricRecord(
                metric_name="risk",
                value=0.3,
                direction=ObjectiveDirection.MINIMIZE,
            ),
        ],
    )
    # c3 is mixed compared to c1
    c3 = CandidateComparisonRecord(
        comparison_id="comp3",
        candidate_id="c3",
        raw_simulation_ref="ref3",
        metrics=[
            TournamentMetricRecord(
                metric_name="quality",
                value=0.9,
                direction=ObjectiveDirection.MAXIMIZE,
            ),
            TournamentMetricRecord(
                metric_name="risk",
                value=0.5,
                direction=ObjectiveDirection.MINIMIZE,
            ),
        ],
    )

    fronts = compute_pareto_fronts([c1, c2, c3], ["quality", "risk"])

    assert len(fronts) == 2
    assert fronts[0].front_index == 1
    assert set(fronts[0].candidate_ids) == {"c1", "c3"}

    assert fronts[1].front_index == 2
    assert set(fronts[1].candidate_ids) == {"c2"}


def test_pareto_fronts_with_cycle():
    # If c1 dominates c2, c2 dominates c3, and c3 dominates c1 (a cycle),
    # all three should be in the first Pareto front, rather than an
    # infinite loop.

    # We will mock compute_dominance_relations briefly to inject a cycle
    # since creating a true cycle with standard metrics is mathematically
    # impossible with transitivity, but bugs in objective direction or
    # multi-metric edge cases could theoretically create one,
    # and the SCC logic is meant to protect against it.

    c1 = CandidateComparisonRecord(
        comparison_id="comp1",
        candidate_id="c1",
        raw_simulation_ref="ref1",
        metrics=[
            TournamentMetricRecord(
                metric_name="M1",
                value=1,
                direction=ObjectiveDirection.MAXIMIZE,
            )
        ],
    )
    c2 = CandidateComparisonRecord(
        comparison_id="comp2",
        candidate_id="c2",
        raw_simulation_ref="ref2",
        metrics=[
            TournamentMetricRecord(
                metric_name="M1",
                value=1,
                direction=ObjectiveDirection.MAXIMIZE,
            )
        ],
    )
    c3 = CandidateComparisonRecord(
        comparison_id="comp3",
        candidate_id="c3",
        raw_simulation_ref="ref3",
        metrics=[
            TournamentMetricRecord(
                metric_name="M1",
                value=1,
                direction=ObjectiveDirection.MAXIMIZE,
            )
        ],
    )

    import sports_signal_bot.tournaments.pareto as pareto

    original_dominates = pareto.dominates

    def mock_dominates(cand_a, cand_b, req):
        if cand_a.candidate_id == "c1" and cand_b.candidate_id == "c2":
            return True, ["M1"]
        if cand_a.candidate_id == "c2" and cand_b.candidate_id == "c3":
            return True, ["M1"]
        if cand_a.candidate_id == "c3" and cand_b.candidate_id == "c1":
            return True, ["M1"]
        return False, []

    try:
        pareto.dominates = mock_dominates
        fronts = compute_pareto_fronts([c1, c2, c3], ["M1"])

        assert len(fronts) == 1
        assert fronts[0].front_index == 1
        assert set(fronts[0].candidate_ids) == {"c1", "c2", "c3"}
    finally:
        pareto.dominates = original_dominates
