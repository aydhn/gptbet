import pytest
from sports_signal_bot.continuity_verification_hardening.budgets import (
    build_continuity_verification_budgets,
    measure_continuity_verification_budget_consumption,
    summarize_continuity_verification_budgets
)

def test_build_and_summarize_budgets():
    budgets = build_continuity_verification_budgets()
    assert budgets["observatory_federation_budget_ms"] == 5000

    consumptions = {
        "observatory_federation_budget_ms": 6000 # Exceeds budget
    }

    summary = summarize_continuity_verification_budgets(budgets, consumptions)
    assert summary["observatory_federation_budget_ms"]["within_budget"] is False
