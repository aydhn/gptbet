from pydantic import Field
from pydantic import BaseModel
from typing import List, Optional, Dict

class BudgetConsumptionRecord(BaseModel):
    consumption_id: str
    amount: float
    description: str

class OperationalResilienceBudgetHealthRecord(BaseModel):
    budget_id: str
    budget_type: str # e.g., handoff_lag, residue, visibility_loss
    allocated: float
    consumed: float = 0.0
    consumptions: List[BudgetConsumptionRecord] = Field(default_factory=list)

    @property
    def is_breached(self) -> bool:
        return self.consumed > self.allocated

def build_operational_resilience_budgets() -> List[OperationalResilienceBudgetHealthRecord]:
    return [
        OperationalResilienceBudgetHealthRecord(budget_id="b_handoff", budget_type="handoff_lag", allocated=10.0),
        OperationalResilienceBudgetHealthRecord(budget_id="b_residue", budget_type="residue", allocated=5.0),
        OperationalResilienceBudgetHealthRecord(budget_id="b_visibility", budget_type="visibility_loss", allocated=0.0) # Zero tolerance for visibility loss ideally
    ]

def measure_operational_resilience_budget_consumption(budget: OperationalResilienceBudgetHealthRecord, consumption: BudgetConsumptionRecord) -> None:
    budget.consumptions.append(consumption)
    budget.consumed += consumption.amount

def summarize_operational_resilience_budgets(budgets: List[OperationalResilienceBudgetHealthRecord]) -> Dict:
    return {
        b.budget_id: {
            "type": b.budget_type,
            "allocated": b.allocated,
            "consumed": b.consumed,
            "is_breached": b.is_breached
        } for b in budgets
    }
