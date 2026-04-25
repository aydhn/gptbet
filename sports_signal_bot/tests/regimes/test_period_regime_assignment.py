import pytest

from sports_signal_bot.regimes.inputs import build_period_regime_inputs
from sports_signal_bot.regimes.period.performance import \
    PerformanceRegimeClassifier
from sports_signal_bot.regimes.thresholds import RegimeThresholdsConfig


def test_performance_regime_assignment():
    config = RegimeThresholdsConfig()
    classifier = PerformanceRegimeClassifier(config)

    inputs = build_period_regime_inputs(
        period_id=1,
        sport="football",
        market_type="1x2",
        historical_metrics=[{"log_loss": 0.60}, {"log_loss": 0.65}],
    )
    records = classifier.assign_period_regimes(inputs)
    assert len(records) == 1
    assert records[0].regime_label == "degrading"
