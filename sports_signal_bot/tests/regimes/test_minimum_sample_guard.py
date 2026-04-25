import pytest

from sports_signal_bot.regimes.contracts import EventRegimeRecord
from sports_signal_bot.regimes.coverage import calculate_coverage
from sports_signal_bot.regimes.thresholds import RegimeThresholdsConfig


def test_minimum_sample_guard():
    config = RegimeThresholdsConfig()
    config.minimum_rows_per_regime = 100

    records = [
        EventRegimeRecord(
            event_id="1",
            sport="f",
            regime_family="form",
            regime_label="hot",
            assignment_method="rule",
        ),
    ]

    covs = calculate_coverage(records, config)
    assert len(covs) == 1
    assert not covs[0].minimum_rows_satisfied
    assert "Low sample size" in covs[0].warnings[0]
