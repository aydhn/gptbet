import pytest

from sports_signal_bot.regimes.contracts import EventRegimeRecord
from sports_signal_bot.regimes.coverage import calculate_coverage
from sports_signal_bot.regimes.thresholds import RegimeThresholdsConfig


def test_regime_coverage():
    config = RegimeThresholdsConfig()
    config.minimum_rows_per_regime = 2

    records = [
        EventRegimeRecord(
            event_id="1",
            sport="f",
            regime_family="form",
            regime_label="both_hot",
            assignment_method="rule",
        ),
        EventRegimeRecord(
            event_id="2",
            sport="f",
            regime_family="form",
            regime_label="both_hot",
            assignment_method="rule",
        ),
        EventRegimeRecord(
            event_id="3",
            sport="f",
            regime_family="form",
            regime_label="both_cold",
            assignment_method="rule",
        ),
    ]

    coverages = calculate_coverage(records, config)
    assert len(coverages) == 2
    hot_cov = next(c for c in coverages if c.regime_label == "both_hot")
    assert hot_cov.row_count == 2
    assert hot_cov.minimum_rows_satisfied is True

    cold_cov = next(c for c in coverages if c.regime_label == "both_cold")
    assert cold_cov.row_count == 1
    assert cold_cov.minimum_rows_satisfied is False
