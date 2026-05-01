from typing import Dict, Any, List, Optional
import uuid
from .contracts import (
    PlaneBudgetRecord, BudgetDelegationRecord, BudgetTransferRecord, BudgetViolationRecord
)

def allocate_local_plane_budget(plane_id: str, budget_type: str, amount: float) -> PlaneBudgetRecord:
    return PlaneBudgetRecord(
        budget_id=f"bud_{uuid.uuid4().hex[:8]}",
        plane_id=plane_id,
        budget_type=budget_type,
        total_amount=amount,
        used_amount=0.0,
        reserved_amount=0.0
    )

def reserve_budget_from_parent(parent_budget: PlaneBudgetRecord, amount: float) -> bool:
    available = parent_budget.total_amount - parent_budget.used_amount - parent_budget.reserved_amount
    if available >= amount:
        parent_budget.reserved_amount += amount
        return True
    return False

def transfer_budget_if_allowed(source: PlaneBudgetRecord, target: PlaneBudgetRecord, amount: float) -> Optional[BudgetTransferRecord]:
    available = source.total_amount - source.used_amount - source.reserved_amount
    if available >= amount and source.budget_type == target.budget_type:
        source.total_amount -= amount
        target.total_amount += amount
        return BudgetTransferRecord(
            transfer_id=f"trx_{uuid.uuid4().hex[:8]}",
            source_plane_id=source.plane_id,
            target_plane_id=target.plane_id,
            amount=amount,
            budget_type=source.budget_type
        )
    return None

def detect_budget_violation(budget: PlaneBudgetRecord, attempted_amount: float) -> Optional[BudgetViolationRecord]:
    available = budget.total_amount - budget.used_amount - budget.reserved_amount
    if attempted_amount > available:
        return BudgetViolationRecord(
            violation_id=f"viol_{uuid.uuid4().hex[:8]}",
            plane_id=budget.plane_id,
            budget_type=budget.budget_type,
            attempted_amount=attempted_amount,
            available_amount=available
        )
    return None

def summarize_budget_tree(budgets: List[PlaneBudgetRecord]) -> Dict[str, Any]:
    summary = {}
    for b in budgets:
        summary[b.plane_id] = {
            "type": b.budget_type,
            "total": b.total_amount,
            "used": b.used_amount,
            "reserved": b.reserved_amount,
            "available": b.total_amount - b.used_amount - b.reserved_amount
        }
    return summary
