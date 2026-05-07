from dataclasses import dataclass, field
from typing import List

@dataclass
class MeshFederationBudgetRecord:
    budget_id: str
    max_stale_members: int

@dataclass
class SuperchainBudgetRecord:
    budget_id: str
    max_stale_segments: int

@dataclass
class SchedulerBusBudgetRecord:
    budget_id: str
    max_drift_ms: int

@dataclass
class CadenceOrchestrationBudgetRecord:
    budget_id: str
    max_missing_acks: int

@dataclass
class BudgetConsumptionRecord:
    consumption_id: str
    consumed: int

@dataclass
class BudgetBreachRecord:
    breach_id: str
    description: str

@dataclass
class GlobalCadenceBudgetWarningRecord:
    warning_id: str
    description: str

@dataclass
class GlobalCadenceBudgetHealthRecord:
    is_healthy: bool
    breaches: List[BudgetBreachRecord]

@dataclass
class GlobalCadenceBudgetManifestRecord:
    manifest_id: str

@dataclass
class GlobalCadenceBudgetsRecord:
    budget_id: str
    mesh_federation_budgets: List[MeshFederationBudgetRecord] = field(default_factory=list)
    superchain_budgets: List[SuperchainBudgetRecord] = field(default_factory=list)
    scheduler_bus_budgets: List[SchedulerBusBudgetRecord] = field(default_factory=list)
    cadence_budgets: List[CadenceOrchestrationBudgetRecord] = field(default_factory=list)
    warnings: List[GlobalCadenceBudgetWarningRecord] = field(default_factory=list)

def build_global_cadence_budgets(budget_id: str) -> GlobalCadenceBudgetsRecord:
    return GlobalCadenceBudgetsRecord(budget_id=budget_id)

def measure_global_cadence_budget_consumption(budgets: GlobalCadenceBudgetsRecord, state: dict) -> GlobalCadenceBudgetHealthRecord:
    breaches = []

    stale_members = state.get("stale_members", 0)
    for b in budgets.mesh_federation_budgets:
        if stale_members > b.max_stale_members:
            breaches.append(BudgetBreachRecord(breach_id=f"breach_{b.budget_id}", description="Max stale members exceeded"))

    stale_segments = state.get("stale_segments", 0)
    for scb in budgets.superchain_budgets:
        if stale_segments > scb.max_stale_segments:
            breaches.append(BudgetBreachRecord(breach_id=f"breach_{scb.budget_id}", description="Max stale segments exceeded"))

    drift_ms = state.get("drift_ms", 0)
    for sbb in budgets.scheduler_bus_budgets:
        if drift_ms > sbb.max_drift_ms:
            breaches.append(BudgetBreachRecord(breach_id=f"breach_{sbb.budget_id}", description="Max drift ms exceeded"))

    missing_acks = state.get("missing_acks", 0)
    for cb in budgets.cadence_budgets:
        if missing_acks > cb.max_missing_acks:
            breaches.append(BudgetBreachRecord(breach_id=f"breach_{cb.budget_id}", description="Max missing acks exceeded"))

    is_healthy = len(breaches) == 0
    return GlobalCadenceBudgetHealthRecord(is_healthy=is_healthy, breaches=breaches)

def summarize_global_cadence_budgets(budgets: GlobalCadenceBudgetsRecord) -> dict:
    return {
        "id": budgets.budget_id,
        "mesh_federation_budgets_count": len(budgets.mesh_federation_budgets),
        "superchain_budgets_count": len(budgets.superchain_budgets),
        "scheduler_bus_budgets_count": len(budgets.scheduler_bus_budgets),
        "cadence_budgets_count": len(budgets.cadence_budgets),
        "warnings_count": len(budgets.warnings)
    }
