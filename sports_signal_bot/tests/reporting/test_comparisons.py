import pytest
from sports_signal_bot.reporting.comparisons import classify_improvement_or_regression, compare_metric_periods, detect_significant_metric_shift

def test_classify_improvement_or_regression():
    assert classify_improvement_or_regression(6.0, "higher_is_better", 5.0) == "improved"
    assert classify_improvement_or_regression(-6.0, "higher_is_better", 5.0) == "degraded"
    assert classify_improvement_or_regression(4.0, "higher_is_better", 5.0) == "stable"

def test_compare_metric_periods():
    comp = compare_metric_periods("test_metric", 110.0, 100.0, "higher_is_better")
    assert comp.delta_abs == 10.0
    assert comp.delta_pct == 10.0
    assert comp.classification == "improved"

def test_detect_significant_metric_shift():
    comp = compare_metric_periods("test_metric", 120.0, 100.0, "higher_is_better")
    assert detect_significant_metric_shift(comp, threshold=15.0) is True
