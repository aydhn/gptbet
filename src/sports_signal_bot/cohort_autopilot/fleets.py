from typing import List
from .contracts import (
    CohortFleetRecord, FleetRiskBudgetRecord, FleetGrowthQuotaRecord,
    FleetAutopilotPressureRecord
)

def build_cohort_fleet(fleet_id: str, cohort_ids: List[str]) -> CohortFleetRecord:
    return CohortFleetRecord(
        fleet_id=fleet_id,
        active_cohort_ids=cohort_ids
    )

def compute_fleet_risk_budget(fleet: CohortFleetRecord, base_budget: float) -> FleetRiskBudgetRecord:
    return FleetRiskBudgetRecord(
        budget_id=f"budget_{fleet.fleet_id}",
        max_risk_score=base_budget,
        current_risk_score=len(fleet.active_cohort_ids) * 0.1 # Mock calculation
    )

def enforce_growth_quota(fleet: CohortFleetRecord, max_growing: int) -> FleetGrowthQuotaRecord:
    return FleetGrowthQuotaRecord(
        quota_id=f"quota_{fleet.fleet_id}",
        max_growing_cohorts=max_growing,
        current_growing_cohorts=min(len(fleet.active_cohort_ids), max_growing)
    )

def summarize_fleet_autopilot_state(fleet: CohortFleetRecord) -> dict:
    return {
        "fleet_id": fleet.fleet_id,
        "active_cohorts": len(fleet.active_cohort_ids)
    }

def suppress_growth_under_fleet_pressure(fleet: CohortFleetRecord, threshold: int) -> FleetAutopilotPressureRecord:
    level = "high" if len(fleet.active_cohort_ids) > threshold else "normal"
    return FleetAutopilotPressureRecord(
        pressure_id=f"pressure_{fleet.fleet_id}",
        pressure_level=level
    )
