import pytest

from sports_signal_bot.signal_scoring.contracts import (
    SignalComponentRecord,
    SignalScoreRecord,
)
from sports_signal_bot.thresholds.strategies.score_and_edge import (
    ScoreAndEdgeThresholdOptimizer,
)


def test_score_and_edge_optimizer():
    optimizer = ScoreAndEdgeThresholdOptimizer(
        {
            "score_threshold_bounds": [0.4, 0.6],
            "edge_threshold_bounds": [0.0, 0.1],
            "grid_steps": 2,
        }
    )

    grid = optimizer.generate_grid()
    assert len(grid) == 4

    signals = [
        SignalScoreRecord(
            event_id="e_0",
            sport="football",
            market_type="1x2",
            selection="home",
            final_probability=0.6,
            components=SignalComponentRecord(edge_estimate=0.05),
            final_signal_score=0.5,
            strategy_name="test",
        ),
        SignalScoreRecord(
            event_id="e_1",
            sport="football",
            market_type="1x2",
            selection="home",
            final_probability=0.6,
            components=SignalComponentRecord(edge_estimate=0.15),
            final_signal_score=0.5,
            strategy_name="test",
        ),
    ]

    acc, rej = optimizer.apply_threshold(
        signals, {"score_threshold": 0.5, "edge_threshold": 0.1}
    )
    assert len(acc) == 1
    assert len(rej) == 1
    assert acc[0].event_id == "e_1"
