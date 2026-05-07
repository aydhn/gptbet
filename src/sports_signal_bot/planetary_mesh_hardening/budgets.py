from .contracts import BusMeshBudgetRecord, BudgetConsumptionRecord

def build_global_scheduler_budgets() -> list:
    return [BusMeshBudgetRecord(budget_id="budget_1")]

def measure_global_scheduler_budget_consumption(budgets: list) -> list:
    return [BudgetConsumptionRecord(consumption_id="cons_1")]

def summarize_global_scheduler_budgets(budgets: list) -> dict:
    return {"total": len(budgets)}
