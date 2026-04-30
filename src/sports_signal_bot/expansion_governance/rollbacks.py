from typing import List, Dict, Any, Tuple
import uuid
from .contracts import (
    SelectiveRollbackDirectiveRecord, RollbackCapacityRecord, ExpansionControlStateRecord, ExpansionStatus
)

def build_selective_rollback_plan(
    reason: str,
    candidates: List[Dict[str, Any]],
    capacity: RollbackCapacityRecord,
    strategy: str = "budget_heavy_first"
) -> Tuple[SelectiveRollbackDirectiveRecord, List[str]]:
    """Builds a plan for selective rollback without breaching rollback capacity."""

    ranked_candidates = rank_rollback_candidates(candidates, strategy)

    selected_cohorts = []
    selected_families = set()
    capacity_used = 0
    warnings = []

    for c in ranked_candidates:
        if capacity_used < capacity.available_capacity:
            selected_cohorts.append(c['cohort_id'])
            if 'cohort_family' in c:
                selected_families.add(c['cohort_family'])
            capacity_used += 1
        else:
            warnings.append(f"Rollback capacity exhausted. Could not include cohort {c['cohort_id']}.")

    directive = SelectiveRollbackDirectiveRecord(
        directive_id=f"rbk_{uuid.uuid4().hex[:8]}",
        reason=reason,
        target_cohorts=selected_cohorts,
        target_families=list(selected_families),
        rollback_level="LEVEL_0_REFERENCE_ONLY"  # Default safe level
    )

    return directive, warnings

def rank_rollback_candidates(candidates: List[Dict[str, Any]], strategy: str) -> List[Dict[str, Any]]:
    """Ranks cohorts to determine which should be rolled back first."""
    if strategy == "budget_heavy_first":
        # Assume 'budget_cost' is present, sort descending
        return sorted(candidates, key=lambda c: c.get('budget_cost', 0), reverse=True)
    elif strategy == "highest_risk_first":
        # Assume 'health_score' is present, sort ascending (lower health = higher risk)
        return sorted(candidates, key=lambda c: c.get('health_score', 100.0))
    else:
        # Default fallback, just return as-is
        return candidates

def execute_selective_rollback(state: ExpansionControlStateRecord, directive: SelectiveRollbackDirectiveRecord) -> Dict[str, Any]:
    """Applies the selective rollback to the control state."""

    # In reality, this would trigger lower-level cohort operations.
    # Here, we update the global state tracking.

    # Remove from active lists if they are completely rolled back
    if directive.rollback_level == "LEVEL_0_REFERENCE_ONLY":
        state.active_cohort_ids = [cid for cid in state.active_cohort_ids if cid not in directive.target_cohorts]

    state.warnings.append(f"Executed selective rollback {directive.directive_id} targeting {len(directive.target_cohorts)} cohorts. Reason: {directive.reason}")

    # Enter rollback stabilization mode if multiple families affected
    if len(directive.target_families) > 1 and state.global_status != ExpansionStatus.GLOBAL_EMERGENCY_PAUSE:
        state.global_status = ExpansionStatus.ROLLBACK_STABILIZATION_MODE

    return {
        "directive_id": directive.directive_id,
        "cohorts_rolled_back": len(directive.target_cohorts),
        "families_affected": directive.target_families,
        "new_global_status": state.global_status.value
    }

def summarize_selective_rollback_outcome(outcome: Dict[str, Any]) -> str:
    """Provides a human-readable summary of the rollback execution."""
    return f"Rollback {outcome['directive_id']} executed: {outcome['cohorts_rolled_back']} cohorts across {len(outcome['families_affected'])} families rolled back. State changed to {outcome['new_global_status']}."
