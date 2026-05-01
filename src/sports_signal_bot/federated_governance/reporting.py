from typing import Dict, Any, List
from .contracts import (
    ControlPlaneRecord, DelegatedActionRecord, EscalationCaseRecord,
    BudgetViolationRecord, PlaneSuspensionRecord, EmergencyOverrideRecord
)

def extract_federated_kpis(
    planes: List[ControlPlaneRecord],
    actions: List[DelegatedActionRecord],
    escalations: List[EscalationCaseRecord],
    violations: List[BudgetViolationRecord],
    suspensions: List[PlaneSuspensionRecord],
    overrides: List[EmergencyOverrideRecord]
) -> Dict[str, float]:

    total_actions = max(len(actions), 1)

    return {
        "delegated_action_rate": len(actions) / max(len(planes), 1),
        "escalation_rate": len(escalations) / total_actions,
        "budget_violation_rate": len(violations) / total_actions,
        "plane_suspension_rate": len(suspensions) / max(len(planes), 1),
        "global_override_frequency": len(overrides) / max(len(planes), 1)
    }

def generate_federated_governance_summary(
    planes: List[ControlPlaneRecord],
    actions: List[DelegatedActionRecord],
    escalations: List[EscalationCaseRecord],
    violations: List[BudgetViolationRecord],
    suspensions: List[PlaneSuspensionRecord],
    overrides: List[EmergencyOverrideRecord]
) -> Dict[str, Any]:
    return {
        "active_plane_count": len([p for p in planes if p.active_status]),
        "delegated_action_count": len(actions),
        "escalation_counts": len(escalations),
        "suspensions": len(suspensions),
        "budget_violations": len(violations),
        "overrides_states": len([o for o in overrides if o.active])
    }
