from src.sports_signal_bot.supermesh_hardening.budgets import build_supermesh_fabric_budgets, evaluate_budget_breaches
from src.sports_signal_bot.supermesh_hardening.contracts import BudgetBreachRecord

def test_breach_without_critical_loss_is_healthy():
    manifest = build_supermesh_fabric_budgets()
    evaluate_budget_breaches(manifest, [BudgetBreachRecord(breach_id="b1", budget_ref="bg1")])
    assert manifest.health.status == "healthy"
    assert len(manifest.health.blockers) == 0

def test_breach_with_no_safe_loss_is_critical():
    manifest = build_supermesh_fabric_budgets()
    evaluate_budget_breaches(manifest, [BudgetBreachRecord(breach_id="b1", budget_ref="bg1", no_safe_loss=True)])
    assert manifest.health.status == "breached"
    assert len(manifest.health.blockers) == 1
    assert "no-safe or sovereignty loss" in manifest.health.blockers[0]
