import pytest

from sports_signal_bot.signal_scoring.contracts import (
    SignalComponentRecord,
    SignalScoreRecord,
)
from sports_signal_bot.thresholds.contracts import ThresholdPolicyRecord
from sports_signal_bot.thresholds.runner import ThresholdRunner


def test_accepted_rejected_records():
    runner = ThresholdRunner({})
    policy = ThresholdPolicyRecord(
        policy_name="test_policy",
        sport="football",
        market_type="1x2",
        signal_strategy="score_only",
        threshold_type="score",
        selected_threshold=0.55,
        optimization_objective="balanced",
    )

    signals = [
        SignalScoreRecord(
            event_id=f"e_{i}",
            sport="football",
            market_type="1x2",
            selection="home",
            final_probability=0.6,
            components=SignalComponentRecord(
                edge_estimate=0.05, confidence_score=0.8, uncertainty_penalty=0.1
            ),
            final_signal_score=0.45 + (i * 0.05),
            strategy_name="test",
        )
        for i in range(5)
    ]

    res = runner.apply_policy(policy, signals)

    accepted = [r for r in res if r.is_accepted]
    rejected = [r for r in res if not r.is_accepted]

    assert len(accepted) == 3
    assert len(rejected) == 2

    # Check fields in exported record
    acc0 = accepted[0]
    assert acc0.event_id in ["e_2", "e_3", "e_4"]
    assert acc0.policy_used == "test_policy"
    assert "score_threshold" in acc0.threshold_values
    assert acc0.threshold_values["score_threshold"] == 0.55
    assert "confidence" in acc0.component_snapshots
    assert "uncertainty" in acc0.component_snapshots
