import pytest
from sports_signal_bot.concurrency_hardening.regressions import compare_concurrency_baselines, classify_concurrency_regression
from sports_signal_bot.concurrency_hardening.contracts import ConcurrencyBaselineRecord, ConcurrencyComparisonRecord

def test_compare_concurrency_baselines():
    base = ConcurrencyBaselineRecord(baseline_id="b1", metrics={"races": 0, "drifts": 0})
    curr = ConcurrencyComparisonRecord(comparison_id="c1", metrics={"races": 1, "drifts": 0})
    regressions = compare_concurrency_baselines(base, curr)
    assert "races" in regressions
    assert "drifts" not in regressions

def test_classify_concurrency_regression():
    sev1 = classify_concurrency_regression("races", 0, 1)
    assert sev1.level == "release_blocking"

    sev2 = classify_concurrency_regression("drift_ms", 10, 50)
    assert sev2.level == "high"
