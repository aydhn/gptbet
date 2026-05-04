import pytest
from sports_signal_bot.resilience_synthesis.debt_ledgers import (
    build_convergence_debt_ledger,
    register_convergence_debt_entry
)
from sports_signal_bot.resilience_synthesis.debt_aging import (
    age_debt_entries,
    escalate_debt_severity_with_age
)

def test_build_convergence_debt_ledger():
    ledger = build_convergence_debt_ledger("l1", "sovereign_convergence_debt_ledger")
    assert ledger.convergence_debt_ledger_id == "l1"
    assert ledger.ledger_family == "sovereign_convergence_debt_ledger"

def test_register_convergence_debt_entry():
    ledger = build_convergence_debt_ledger("l1", "sovereign_convergence_debt_ledger")
    entry = register_convergence_debt_entry(ledger, "d1", "unresolved_successor_debt", "moderate")
    assert entry.debt_entry_id == "d1"
    assert entry.debt_severity.level == "moderate"
    assert len(ledger.active_debt_entry_refs) == 1

def test_debt_aging():
    ledger = build_convergence_debt_ledger("l1", "sovereign_convergence_debt_ledger")
    entry = register_convergence_debt_entry(ledger, "d1", "unresolved_successor_debt", "moderate")
    age_debt_entries([entry], 40)
    assert entry.debt_age.days_old == 40
    escalate_debt_severity_with_age(entry)
    assert entry.debt_severity.level == "high"
