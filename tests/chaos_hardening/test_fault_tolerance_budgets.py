import pytest
from sports_signal_bot.chaos_hardening.contracts import FaultToleranceBudgetRecord

def test_budget():
    budget = FaultToleranceBudgetRecord(budget_id="b1", error_budgets=[])
    assert budget.budget_id == "b1"
