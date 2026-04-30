import pytest
from sports_signal_bot.stable_adoption.verification import build_post_activation_verification_plan, run_post_activation_checks, detect_post_activation_regression
from sports_signal_bot.stable_adoption.contracts import VerificationWindow

def test_post_activation_verification_clean():
    plan = build_post_activation_verification_plan("adp_01", VerificationWindow.IMMEDIATE_VERIFICATION, ["latency_check", "error_rate_check"])
    result = run_post_activation_checks(plan, {"latency_check": True, "error_rate_check": True})
    assert detect_post_activation_regression(result) is False

def test_post_activation_verification_fail():
    plan = build_post_activation_verification_plan("adp_01", VerificationWindow.IMMEDIATE_VERIFICATION, ["latency_check", "error_rate_check"])
    result = run_post_activation_checks(plan, {"latency_check": True, "error_rate_check": False})
    assert detect_post_activation_regression(result) is True
