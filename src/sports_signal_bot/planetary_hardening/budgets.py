import uuid
from typing import List
from src.sports_signal_bot.planetary_hardening.contracts import (
    PlanetaryResilienceBudgetManifestRecord,
    PlanetaryCoverageBudgetRecord,
    IntercontinentalLaneBudgetRecord,
    QuorumFederationBudgetRecord,
    FollowTheSunAuditBudgetRecord,
    BudgetConsumptionRecord,
    BudgetBreachRecord
)

def build_planetary_resilience_budgets() -> PlanetaryResilienceBudgetManifestRecord:
    return PlanetaryResilienceBudgetManifestRecord(
        manifest_id=f"budget_{uuid.uuid4().hex[:8]}",
        planetary_budgets=[PlanetaryCoverageBudgetRecord(budget_id="pcc_b1", max_seam_gap_hours=1.0)],
        lane_budgets=[IntercontinentalLaneBudgetRecord(budget_id="icl_b1", max_lag_hours=2.0)],
        quorum_budgets=[QuorumFederationBudgetRecord(budget_id="qf_b1", max_asymmetry_score=0.1)],
        audit_budgets=[FollowTheSunAuditBudgetRecord(budget_id="fts_b1", max_handoff_lag_hours=0.5)]
    )

def measure_planetary_budget_consumption(manifest: PlanetaryResilienceBudgetManifestRecord, consumption: BudgetConsumptionRecord, budget_type: str) -> PlanetaryResilienceBudgetManifestRecord:
    # Simplified check
    if consumption.amount > 2.0:
        manifest.breaches.append(BudgetBreachRecord(breach_id=f"breach_{uuid.uuid4().hex[:8]}", description=f"Budget breached for {budget_type}"))
    return manifest

def summarize_planetary_resilience_budgets(manifest: PlanetaryResilienceBudgetManifestRecord) -> dict:
    return {
        "id": manifest.manifest_id,
        "breaches_count": len(manifest.breaches)
    }
