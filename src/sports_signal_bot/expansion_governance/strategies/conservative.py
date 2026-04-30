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

class ConservativeExpansionGovernanceStrategy(BaseExpansionGovernanceStrategy):
    """
    Default conservative strategy.
    Strict budget and pressure boundaries, high circuit breaker sensitivity.
    """

    def evaluate_state(self, metrics: Dict[str, Any]) -> ExpansionGovernanceManifest:
        state = ExpansionControlStateRecord(
            control_state_id=f"cs_{uuid.uuid4().hex[:8]}",
            active_cohort_ids=metrics.get('active_cohorts', []),
            active_wave_ids=metrics.get('active_waves', [])
        )

        # Mocks for demonstration; in reality these would be passed in or built from deeper state
        budgets = []
        if 'budget_usage' in metrics:
            budgets.append(ExpansionBudgetRecord(
                budget_id="b_main", budget_family="adoption_risk_budget",
                total_budget=100.0, used_budget=metrics['budget_usage'] * 100, remaining_budget=100.0 - (metrics['budget_usage'] * 100),
                budget_status="healthy" if metrics['budget_usage'] < 0.6 else ("exhausted" if metrics['budget_usage'] > 0.9 else "critical")
            ))

        pressure = compute_global_pressure(
            active_cohort_count=len(state.active_cohort_ids),
            simultaneously_growing_cohort_count=metrics.get('growing_cohorts', 0),
            family_conflict_burden=metrics.get('conflict_burden', 0.0),
            verification_warning_density=metrics.get('warning_density', 0.0),
            review_backlog_pressure=metrics.get('review_backlog', 0.0),
            dispute_burden=metrics.get('dispute_burden', 0.0),
            rollback_recentness_penalty=metrics.get('rollback_penalty', 0.0),
            budget_saturation=metrics.get('budget_usage', 0.0)
        )

        # Increase pressure artificially for conservative strategy
        if pressure.pressure_score > 0.4:
            from ..contracts import PressureBand
            pressure.pressure_score = min(pressure.pressure_score + 0.2, 1.0)
            if pressure.pressure_score >= 0.85: pressure.pressure_band = PressureBand.CRITICAL
            elif pressure.pressure_score >= 0.70: pressure.pressure_band = PressureBand.SEVERE
            elif pressure.pressure_score >= 0.50: pressure.pressure_band = PressureBand.HIGH

        conflicts = detect_cross_cohort_conflicts(metrics.get('cohort_details', []))
        breakers = evaluate_circuit_breakers(state, metrics)

        return self._build_manifest(state, budgets, pressure, conflicts, breakers)
