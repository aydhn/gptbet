import pytest
from datetime import datetime, timedelta
from sports_signal_bot.governance_exceptions.contracts import SovereignGovernanceExceptionLedgerRecord, GovernanceExceptionRecord
from sports_signal_bot.governance_exceptions.exceptions import build_governance_exception_ledger, open_governance_exception, evaluate_exception_expiry

def test_build_governance_exception_ledger():
    ledger = build_governance_exception_ledger("ledger_family", "scope_1")
    assert ledger.ledger_family == "ledger_family"
    assert ledger.owning_scope_ref == "scope_1"

def test_open_governance_exception():
    exception = open_governance_exception(
        "temporary_review_visibility_exception",
        "opened_reason",
        "scope_1",
        3600
    )
    assert exception.exception_family == "temporary_review_visibility_exception"
    assert exception.validity_window == 3600
    assert exception.decision_status == "exception_opened"

def test_evaluate_exception_expiry():
    exception = open_governance_exception(
        "temporary_review_visibility_exception",
        "opened_reason",
        "scope_1",
        3600
    )
    created_at = datetime.now()
    # Not expired
    assert evaluate_exception_expiry(exception, created_at + timedelta(seconds=1800), created_at) == "retain_exception_caveated"
    # Expired
    assert evaluate_exception_expiry(exception, created_at + timedelta(seconds=3601), created_at) == "expire_exception"
