from typing import Dict, Any, List
import uuid
from .base import BaseExpansionGovernanceStrategy
from ..contracts import (
    ExpansionControlStateRecord, ExpansionBudgetRecord, ExpansionPressureRecord,
    CrossCohortConflictRecord, BreakerEvaluationRecord, ExpansionGovernanceManifest
)
from ..pressure import compute_global_pressure
from ..breakers import evaluate_circuit_breakers
from ..conflicts import detect_cross_cohort_conflicts

class FamilyFirstProtectionStrategy(BaseExpansionGovernanceStrategy):
    """
    Family-first protection strategy.
    Heavily penalizes cross-family collisions and prefers family freezes over global pauses.
    """

    def evaluate_state(self, metrics: Dict[str, Any]) -> ExpansionGovernanceManifest:
        state = ExpansionControlStateRecord(
            control_state_id=f"cs_{uuid.uuid4().hex[:8]}",
            active_cohort_ids=metrics.get('active_cohorts', []),
            active_wave_ids=metrics.get('active_waves', [])
        )

        budgets = []
        if 'budget_usage' in metrics:
            budgets.append(ExpansionBudgetRecord(
                budget_id="b_main", budget_family="family_scope_budget",
                total_budget=100.0, used_budget=metrics['budget_usage'] * 100, remaining_budget=100.0 - (metrics['budget_usage'] * 100),
                budget_status="healthy" if metrics['budget_usage'] < 0.6 else "warning"
            ))

        # Boost conflict burden to simulate family sensitivity
        conflict_burden = metrics.get('conflict_burden', 0.0) * 1.5

        pressure = compute_global_pressure(
            active_cohort_count=len(state.active_cohort_ids),
            simultaneously_growing_cohort_count=metrics.get('growing_cohorts', 0),
            family_conflict_burden=conflict_burden,
            verification_warning_density=metrics.get('warning_density', 0.0),
            review_backlog_pressure=metrics.get('review_backlog', 0.0),
            dispute_burden=metrics.get('dispute_burden', 0.0),
            rollback_recentness_penalty=metrics.get('rollback_penalty', 0.0),
            budget_saturation=metrics.get('budget_usage', 0.0)
        )

        conflicts = detect_cross_cohort_conflicts(metrics.get('cohort_details', []))

        # If we have any medium+ conflict, instantly apply a family freeze simulation via state flags
        if any(c.severity in ["medium", "high", "critical"] for c in conflicts):
            fam = conflicts[0].involved_cohorts[0] if conflicts[0].involved_cohorts else "unknown" # naive mock
            state.family_freeze_states[f"mock_fam_from_{fam}"] = True

        breakers = evaluate_circuit_breakers(state, metrics)

        return self._build_manifest(state, budgets, pressure, conflicts, breakers)
