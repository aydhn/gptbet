from typing import List, Dict, Optional
from datetime import datetime
import uuid
from .contracts import ExpansionBudgetRecord, BudgetBurnRecord, ExpansionWaveRecord

def build_global_risk_budget(budget_family: str, total_budget: float, drivers: List[str]) -> ExpansionBudgetRecord:
    """Builds a new global risk budget record."""
    return ExpansionBudgetRecord(
        budget_id=f"budget_{uuid.uuid4().hex[:8]}",
        budget_family=budget_family,
        total_budget=total_budget,
        used_budget=0.0,
        reserved_budget=0.0,
        remaining_budget=total_budget,
        budget_status="healthy",
        drivers=drivers
    )

def compute_budget_burn(budget: ExpansionBudgetRecord, burn_amount: float, reason: str) -> BudgetBurnRecord:
    """Computes budget burn and returns a burn record. Assumes budget is mutated by caller."""
    return BudgetBurnRecord(
        burn_id=f"burn_{uuid.uuid4().hex[:8]}",
        budget_id=budget.budget_id,
        burned_amount=burn_amount,
        reason=reason
    )

def reserve_budget_for_wave(budget: ExpansionBudgetRecord, wave: ExpansionWaveRecord) -> bool:
    """Attempts to reserve budget for a wave. Returns True if successful."""
    required = wave.budget_cost
    if budget.remaining_budget >= required:
        budget.reserved_budget += required
        budget.remaining_budget -= required
        _update_budget_status(budget)
        return True
    return False

def release_budget_after_pause_or_rollback(budget: ExpansionBudgetRecord, amount: float, was_reserved: bool = False) -> None:
    """Releases budget (either reserved or used) back to remaining."""
    if was_reserved:
        release_amount = min(budget.reserved_budget, amount)
        budget.reserved_budget -= release_amount
    else:
        release_amount = min(budget.used_budget, amount)
        budget.used_budget -= release_amount

    budget.remaining_budget += release_amount
    _update_budget_status(budget)

def summarize_budget_pressure(budgets: List[ExpansionBudgetRecord]) -> Dict[str, float]:
    """Summarizes budget usage percentage across all families."""
    summary = {}
    for b in budgets:
        usage_pct = 0.0
        if b.total_budget > 0:
            usage_pct = (b.used_budget + b.reserved_budget) / b.total_budget
        summary[b.budget_family] = round(usage_pct, 4)
    return summary

def commit_wave_budget(budget: ExpansionBudgetRecord, wave: ExpansionWaveRecord) -> None:
    """Moves reserved budget to used budget when wave activates."""
    required = wave.budget_cost
    transfer = min(budget.reserved_budget, required)
    budget.reserved_budget -= transfer
    budget.used_budget += transfer
    _update_budget_status(budget)

def _update_budget_status(budget: ExpansionBudgetRecord) -> None:
    """Internal helper to update the qualitative status string."""
    usage_pct = 0.0
    if budget.total_budget > 0:
         usage_pct = (budget.used_budget + budget.reserved_budget) / budget.total_budget

    if usage_pct >= 0.95:
        budget.budget_status = "exhausted"
    elif usage_pct >= 0.80:
        budget.budget_status = "critical"
    elif usage_pct >= 0.60:
        budget.budget_status = "warning"
    else:
        budget.budget_status = "healthy"
