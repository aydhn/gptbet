import pytest
from sports_signal_bot.thresholds.strategies.conservative_quality import ConservativeQualityOptimizer
from sports_signal_bot.signal_scoring.contracts import SignalScoreRecord, SignalComponentRecord

def test_conservative_quality_optimizer():
    optimizer = ConservativeQualityOptimizer({
        "score_threshold_bounds": [0.4, 0.6],
        "grid_steps": 2,
        "hard_max_uncertainty": 0.3,
        "hard_max_dq_penalty": 0.2
    })

    signals = [
        SignalScoreRecord(
            event_id="e_0",
            sport="football",
            market_type="1x2",
            selection="home",
            final_probability=0.6,
            components=SignalComponentRecord(uncertainty_penalty=0.1, data_quality_penalty=0.1),
            final_signal_score=0.5,
            strategy_name="test"
        ),
        SignalScoreRecord(
            event_id="e_1",
            sport="football",
            market_type="1x2",
            selection="home",
            final_probability=0.6,
            components=SignalComponentRecord(uncertainty_penalty=0.4, data_quality_penalty=0.1),
            final_signal_score=0.5,
            strategy_name="test"
        )
    ]

    acc, rej = optimizer.apply_threshold(signals, {"score_threshold": 0.4})
    assert len(acc) == 1
    assert len(rej) == 1
    assert acc[0].event_id == "e_0"
