from typing import List, Dict, Any
from .contracts import (
    ExpansionControlStateRecord, ExpansionBudgetRecord, ExpansionPressureRecord,
    BreakerEvaluationRecord, ControlTowerSummaryRecord, ExpansionCouncilRecord
)
from .budgets import summarize_budget_pressure

class ExpansionControlTowerBuilder:
    """Builds the central control tower summary from disparate global state components."""

    @staticmethod
    def build_summary(
        state: ExpansionControlStateRecord,
        budgets: List[ExpansionBudgetRecord],
        pressure: ExpansionPressureRecord,
        breakers: BreakerEvaluationRecord,
        council_decision: ExpansionCouncilRecord
    ) -> ControlTowerSummaryRecord:

        frozen_families = [fam for fam, is_frozen in state.family_freeze_states.items() if is_frozen]

        breaker_state = "Clear"
        if breakers.triggers_fired:
            breaker_state = f"Fired: {len(breakers.triggers_fired)} triggers"

        recommended_actions = [f"Council Decision: {council_decision.decision.value}"]
        if council_decision.decision != "continue_expansion":
            recommended_actions.append(f"Rationale: {council_decision.rationale}")

        return ControlTowerSummaryRecord(
            summary_id=f"ct_{state.control_state_id.split('_')[1] if '_' in state.control_state_id else 'sum'}",
            global_status=state.global_status.value,
            active_waves=len(state.active_wave_ids),
            active_cohorts=len(state.active_cohort_ids),
            budget_usage_summary=summarize_budget_pressure(budgets),
            global_pressure_band=pressure.pressure_band.value,
            family_freezes=frozen_families,
            top_blockers=state.warnings[:3],  # Take top 3 warnings as mock blockers
            emergency_breaker_state=breaker_state,
            recommended_actions=recommended_actions
        )
