import pytest
import pandas as pd
from sports_signal_bot.thresholds.runner import ThresholdRunner
from sports_signal_bot.signal_scoring.contracts import SignalScoreRecord, SignalComponentRecord
from sports_signal_bot.thresholds.contracts import ThresholdPolicyRecord

def test_threshold_runner_sweep():
    config = {
        "sweep_engine": {
            "objective": {"objective_name": "balanced"},
            "constraints": {"minimum_accepted_count": 1},
            "grid": {"score_threshold_bounds": [0.4, 0.6], "grid_steps": 3}
        }
    }
    runner = ThresholdRunner(config)

    signals = [
        SignalScoreRecord(
            event_id=f"e_{i}",
            sport="football",
            market_type="1x2",
            selection="home",
            final_probability=0.6,
            components=SignalComponentRecord(edge_estimate=0.05),
            final_signal_score=0.45 + (i * 0.05),
            strategy_name="test"
        ) for i in range(5)
    ]

    labels_df = pd.DataFrame([
        {"event_id": f"e_{i}", "target_value": "home" if i % 2 == 0 else "away"}
        for i in range(5)
    ])

    res = runner.optimize("score_only", signals, labels_df, "football", "1x2")

    assert res.total_evaluated == 3
    assert res.best_candidate is not None
    assert res.best_candidate.score_threshold >= 0.4

def test_threshold_runner_apply():
    runner = ThresholdRunner({})
    policy = ThresholdPolicyRecord(
        policy_name="test",
        sport="football",
        market_type="1x2",
        signal_strategy="score_only",
        threshold_type="score",
        selected_threshold=0.55,
        optimization_objective="balanced"
    )

    signals = [
        SignalScoreRecord(
            event_id=f"e_{i}",
            sport="football",
            market_type="1x2",
            selection="home",
            final_probability=0.6,
            components=SignalComponentRecord(edge_estimate=0.05),
            final_signal_score=0.45 + (i * 0.05), # 0.45, 0.50, 0.55, 0.60, 0.65
            strategy_name="test"
        ) for i in range(5)
    ]

    res = runner.apply_policy(policy, signals)
    assert len(res) == 5

    accepted = [r for r in res if r.is_accepted]
    assert len(accepted) == 3 # 0.55, 0.60, 0.65
