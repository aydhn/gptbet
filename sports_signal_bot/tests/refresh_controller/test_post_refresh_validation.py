import pytest
from sports_signal_bot.refresh_controller.validation import PostRefreshValidator
from sports_signal_bot.refresh_controller.contracts import RefreshAttempt
from datetime import datetime, timezone

def test_validate_refresh_outcome_success():
    validator = PostRefreshValidator()
    attempt = RefreshAttempt(plan_id="123", status="success")

    assert validator.validate_refresh_outcome(attempt) is True
    assert attempt.validation_passed is True

def test_validate_refresh_outcome_failure():
    validator = PostRefreshValidator()
    attempt = RefreshAttempt(plan_id="123", status="failed")

    assert validator.validate_refresh_outcome(attempt) is False
    assert attempt.validation_passed is False
