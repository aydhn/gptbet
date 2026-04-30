from typing import Dict, Any
from .base import BaseCohortAutopilotStrategy
from ..contracts import (
    AutopilotDecisionRecord, AutopilotAction, ActivationLevel, AdoptionCohortRecord
)
from ..decisions import create_decision

class FleetBudgetAwareStrategy(BaseCohortAutopilotStrategy):
    """
    Çoklu cohort baskısında büyümeyi kısar.
    Risk bütçesi merkezlidir.
    """
    def evaluate(self, cohort: AdoptionCohortRecord, context: Dict[str, Any]) -> AutopilotDecisionRecord:
        blockers = context.get("blockers", [])
        stability = context.get("stability_score", 0.0)
        fleet_pressure = context.get("fleet_pressure", "normal")

        if blockers:
            return create_decision(
                cohort.cohort_id, cohort.activation_level, AutopilotAction.PAUSE_COHORT,
                {"stability": stability}, blockers
            )

        if fleet_pressure == "high":
            return create_decision(
                cohort.cohort_id, cohort.activation_level, AutopilotAction.HOLD_COHORT,
                {"stability": stability, "fleet_pressure_penalty": -0.3}, []
            )

        if stability >= 0.9:
            return create_decision(
                cohort.cohort_id, cohort.activation_level, AutopilotAction.PROGRESS_COHORT,
                {"stability": stability}, []
            )

        return create_decision(
            cohort.cohort_id, cohort.activation_level, AutopilotAction.HOLD_COHORT,
            {"stability": stability}, []
        )
