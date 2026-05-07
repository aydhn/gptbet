from sports_signal_bot.global_hardening.contracts import GlobalResilienceBudgetsRecord, GlobalQuorumBudgetRecord, BudgetConsumptionRecord
from sports_signal_bot.global_hardening.budgets import build_global_resilience_budgets, add_quorum_budget, measure_global_budget_consumption, check_budget_breaches

def test_budget_breach():
    budgets = build_global_resilience_budgets("b1")
    add_quorum_budget(budgets, GlobalQuorumBudgetRecord(budget_id="qb1", limit=100))
    measure_global_budget_consumption(budgets, BudgetConsumptionRecord(consumption_id="c1", amount=150))

    check_budget_breaches(budgets)
    assert len(budgets.breaches) > 0
    assert len(budgets.warnings) > 0
