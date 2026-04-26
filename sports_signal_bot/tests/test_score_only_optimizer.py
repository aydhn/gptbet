import pytest

from sports_signal_bot.signal_scoring.contracts import (SignalComponentRecord,
                                                        SignalScoreRecord)
from sports_signal_bot.thresholds.strategies.score_only import \
    ScoreOnlyThresholdOptimizer


def test_score_only_optimizer():
    optimizer = ScoreOnlyThresholdOptimizer(
        {"score_threshold_bounds": [0.4, 0.6], "grid_steps": 3}
    )

    grid = optimizer.generate_grid()
    assert len(grid) == 3
    assert grid[0]["score_threshold"] == 0.4
    assert grid[1]["score_threshold"] == 0.5
    assert grid[2]["score_threshold"] == 0.6

    signals = [
        SignalScoreRecord(
            event_id=f"e_{i}",
            sport="football",
            market_type="1x2",
            selection="home",
            final_probability=0.6,
            components=SignalComponentRecord(),
            final_signal_score=0.45 + (i * 0.05),  # 0.45, 0.50, 0.55
            strategy_name="test",
        )
        for i in range(3)
    ]

    acc, rej = optimizer.apply_threshold(signals, {"score_threshold": 0.5})
    assert len(acc) == 2  # 0.50, 0.55
    assert len(rej) == 1  # 0.45
