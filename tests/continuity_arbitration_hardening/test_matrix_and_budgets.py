from src.sports_signal_bot.continuity_arbitration_hardening.budgets import ContinuityArbitrationBudgetRecord, measure_continuity_arbitration_budget_consumption

def test_budget_consumption_under_limit():
    budget = ContinuityArbitrationBudgetRecord("1", "test_budget", 100, 50)
    assert measure_continuity_arbitration_budget_consumption(budget, 20) == True
    assert budget.consumed == 70

def test_budget_consumption_over_limit():
    budget = ContinuityArbitrationBudgetRecord("1", "test_budget", 100, 90)
    assert measure_continuity_arbitration_budget_consumption(budget, 20) == False
    assert budget.consumed == 110
