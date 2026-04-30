from typing import Dict, Any
from .base import BaseCohortAutopilotStrategy
from ..contracts import (
    AutopilotDecisionRecord, AutopilotAction, ActivationLevel, AdoptionCohortRecord
)
from ..decisions import create_decision

class ConservativeCohortAutopilotStrategy(BaseCohortAutopilotStrategy):
    """
    Growth yavaş, pause/hold eğilimi yüksek.
    Rollback duyarlılığı fazla.
    """
    def evaluate(self, cohort: AdoptionCohortRecord, context: Dict[str, Any]) -> AutopilotDecisionRecord:
        blockers = context.get("blockers", [])
        stability = context.get("stability_score", 0.0)

        if blockers or stability < 0.95:
            action = AutopilotAction.PAUSE_COHORT if stability >= 0.8 else AutopilotAction.ROLLBACK_COHORT
            return create_decision(
                cohort.cohort_id,
                cohort.activation_level,
                action,
                {"stability": stability, "conservative_penalty": -0.2},
                blockers
            )

        return create_decision(
            cohort.cohort_id,
            cohort.activation_level,
            AutopilotAction.HOLD_COHORT,
            {"stability": stability},
            blockers
        )
