import pytest

from sports_signal_bot.regimes.thresholds import RegimeThresholdsConfig


def test_regime_thresholds_defaults():
    config = RegimeThresholdsConfig()
    assert config.disagreement_thresholds.low == 0.05
    assert config.disagreement_thresholds.high == 0.15
    assert config.short_rest_days == 3
