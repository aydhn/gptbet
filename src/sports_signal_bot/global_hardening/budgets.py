from typing import List
from .contracts import (
    GlobalResilienceBudgetsRecord,
    GlobalQuorumBudgetRecord,
    CoverageBudgetRecord,
    GlobalContinuityBudgetRecord,
    GovernanceApprovalBudgetRecord,
    BudgetConsumptionRecord,
    BudgetBreachRecord,
    GlobalResilienceBudgetWarningRecord
)

def build_global_resilience_budgets(budgets_id: str) -> GlobalResilienceBudgetsRecord:
    return GlobalResilienceBudgetsRecord(
        budgets_id=budgets_id
    )

def add_quorum_budget(budgets: GlobalResilienceBudgetsRecord, budget: GlobalQuorumBudgetRecord) -> None:
    budgets.quorum_budgets.append(budget)

def measure_global_budget_consumption(budgets: GlobalResilienceBudgetsRecord, consumption: BudgetConsumptionRecord) -> None:
    budgets.consumptions.append(consumption)

def check_budget_breaches(budgets: GlobalResilienceBudgetsRecord) -> None:
    # simple mock check
    total_consumption = sum(c.amount for c in budgets.consumptions)
    total_quorum_limit = sum(b.limit for b in budgets.quorum_budgets)
    if total_consumption > total_quorum_limit:
        budgets.breaches.append(BudgetBreachRecord(
            breach_id="breach_01",
            description="quorum budget exceeded"
        ))
        budgets.warnings.append(GlobalResilienceBudgetWarningRecord(
            warning_id="warn_budget",
            message="global resilience budget breached"
        ))

def summarize_global_resilience_budgets(budgets: GlobalResilienceBudgetsRecord) -> dict:
    check_budget_breaches(budgets)
    return {
        "id": budgets.budgets_id,
        "consumptions": len(budgets.consumptions),
        "breaches": len(budgets.breaches),
        "warnings": len(budgets.warnings)
    }
