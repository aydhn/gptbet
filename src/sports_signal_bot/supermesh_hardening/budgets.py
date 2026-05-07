from typing import List
from .contracts import (
    SupermeshBudgetRecord, CadenceFabricBudgetRecord, AuditPulseBudgetRecord,
    HandoffObservatoryBudgetRecord, BudgetConsumptionRecord, BudgetBreachRecord,
    SupermeshFabricBudgetHealthRecord, SupermeshFabricBudgetManifestRecord
)

def build_supermesh_fabric_budgets() -> SupermeshFabricBudgetManifestRecord:
    return SupermeshFabricBudgetManifestRecord(
        health=SupermeshFabricBudgetHealthRecord(status="healthy")
    )

def measure_supermesh_fabric_budget_consumption(manifest: SupermeshFabricBudgetManifestRecord, consumption: BudgetConsumptionRecord):
    manifest.consumptions.append(consumption)

def evaluate_budget_breaches(manifest: SupermeshFabricBudgetManifestRecord, breaches: List[BudgetBreachRecord]):
    manifest.breaches.extend(breaches)
    for breach in breaches:
        if breach.no_safe_loss or breach.sovereignty_loss:
            manifest.health.status = "breached"
            manifest.health.blockers.append(f"Critical breach {breach.breach_id} due to no-safe or sovereignty loss.")

def summarize_supermesh_fabric_budgets(manifest: SupermeshFabricBudgetManifestRecord) -> dict:
    return {
        "status": manifest.health.status,
        "supermesh_budgets": len(manifest.supermesh_budgets),
        "fabric_budgets": len(manifest.fabric_budgets),
        "pulse_budgets": len(manifest.pulse_budgets),
        "observatory_budgets": len(manifest.observatory_budgets),
        "consumptions": len(manifest.consumptions),
        "breaches": len(manifest.breaches),
        "blockers": len(manifest.health.blockers)
    }
