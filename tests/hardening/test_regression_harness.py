import pytest
from sports_signal_bot.hardening.regression import run_regression_case

def test_run_regression_case_matched():
    case = run_regression_case("c1", "f1", "fix1", "gold1", "gold1")
    assert case.result_status == "matched"

def test_run_regression_case_mismatched():
    case = run_regression_case("c1", "f1", "fix1", "gold1", "actual1")
    assert case.result_status == "mismatched"
