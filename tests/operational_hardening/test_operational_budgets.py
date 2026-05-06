from sports_signal_bot.operational_hardening.budgets import build_operational_budgets

def test_operational_budgets():
    assert build_operational_budgets() == {"status": "budgets_built"}
