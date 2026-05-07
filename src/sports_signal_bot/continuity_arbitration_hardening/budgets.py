import uuid
from typing import List, Dict, Any
from datetime import datetime, timezone

class ContinuityArbitrationBudgetRecord:
    def __init__(self, budget_id: str, budget_family: str, limit: int, consumed: int):
        self.budget_id = budget_id
        self.budget_family = budget_family
        self.limit = limit
        self.consumed = consumed

def measure_continuity_arbitration_budget_consumption(budget: ContinuityArbitrationBudgetRecord, new_consumption: int) -> bool:
    budget.consumed += new_consumption
    return budget.consumed <= budget.limit
