from typing import List, Dict, Any
from .contracts import (
    ObservatoryFederationStatus,
    SchedulerProofLaneStatus,
    AuditPulseCouncilStatus,
    ContinuityEvidenceExchangeStatus
)

def build_continuity_verification_budgets() -> Dict[str, Any]:
    return {
        "observatory_federation_budget_ms": 5000,
        "scheduler_proof_budget_ms": 3000,
        "audit_pulse_council_budget_ms": 8000,
        "continuity_evidence_exchange_budget_ms": 4000
    }

def measure_continuity_verification_budget_consumption(actual_ms: int, budget_ms: int) -> bool:
    return actual_ms <= budget_ms

def summarize_continuity_verification_budgets(budgets: Dict[str, Any], consumptions: Dict[str, int]) -> Dict[str, Any]:
    summary = {}
    for key, budget in budgets.items():
        actual = consumptions.get(key, 0)
        summary[key] = {
            "budget_ms": budget,
            "actual_ms": actual,
            "within_budget": measure_continuity_verification_budget_consumption(actual, budget)
        }
    return summary
