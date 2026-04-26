import pytest
from sports_signal_bot.thresholds.contracts import ThresholdCandidateRecord
from sports_signal_bot.thresholds.frontier import ThresholdFrontierBuilder

def test_frontier_builder():
    candidates = [
        ThresholdCandidateRecord(
            market_type="1x2",
            sport="football",
            score_threshold=0.5,
            accepted_count=100,
            rejected_count=0,
            coverage_rate=1.0,
            acceptance_rate=1.0,
            objective_value=0.5,
            quality_metrics={"accuracy": 0.5, "log_loss": 0.69}
        ),
        ThresholdCandidateRecord(
            market_type="1x2",
            sport="football",
            score_threshold=0.6,
            accepted_count=50,
            rejected_count=50,
            coverage_rate=0.5,
            acceptance_rate=0.5,
            objective_value=0.6,
            quality_metrics={"accuracy": 0.6, "log_loss": 0.60}
        )
    ]

    builder = ThresholdFrontierBuilder(candidates, "football", "1x2")
    frontier = builder.build()

    assert len(frontier.tradeoff_curve) == 2

    pt0 = frontier.tradeoff_curve[0]
    assert pt0["score_threshold"] == 0.5
    assert pt0["coverage_rate"] == 1.0
    assert pt0["accuracy"] == 0.5

    summary = builder.summarize_tradeoff_curve(frontier)
    assert summary["max_coverage"] == 1.0
    assert summary["max_objective"] == 0.6
    assert summary["num_points"] == 2
