import pytest

from sports_signal_bot.evaluation.contracts import EvaluationSummaryRecord
from sports_signal_bot.evaluation.leaderboard import build_leaderboard


def test_build_leaderboard():
    s1 = EvaluationSummaryRecord(
        source_name="Model_A",
        source_family="ml",
        sport="football",
        market_type="1x2",
        row_count=100,
        coverage_rate=1.0,
        log_loss=0.65,
        brier=0.20,
        accuracy=0.55,
    )
    s2 = EvaluationSummaryRecord(
        source_name="Model_B",
        source_family="benchmark",
        sport="football",
        market_type="1x2",
        row_count=100,
        coverage_rate=1.0,
        log_loss=0.70,
        brier=0.22,
        accuracy=0.50,
    )

    lb = build_leaderboard([s1, s2], primary_metric="log_loss")

    assert len(lb) == 2
    assert lb[0].source_name == "Model_A"
    assert lb[1].source_name == "Model_B"
    assert lb[0].rank == 1

    # Test sorting by accuracy (higher is better)
    lb2 = build_leaderboard([s1, s2], primary_metric="accuracy")
    assert lb2[0].source_name == "Model_A"
