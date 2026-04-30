from typing import Dict, Any
from .base import BaseCohortAutopilotStrategy
from ..contracts import (
    AutopilotDecisionRecord, AutopilotAction, ActivationLevel, AdoptionCohortRecord
)
from ..decisions import create_decision

class RollbackSensitiveStrategy(BaseCohortAutopilotStrategy):
    """
    Küçük regressions'ta bile kolay pause/rollback.
    Kritik family'ler için uygun.
    """
    def evaluate(self, cohort: AdoptionCohortRecord, context: Dict[str, Any]) -> AutopilotDecisionRecord:
        blockers = context.get("blockers", [])
        stability = context.get("stability_score", 0.0)

        if blockers or stability < 0.99:
            return create_decision(
                cohort.cohort_id, cohort.activation_level, AutopilotAction.ROLLBACK_COHORT,
                {"stability": stability, "rollback_sensitive_penalty": -0.5}, blockers
            )

        return create_decision(
            cohort.cohort_id, cohort.activation_level, AutopilotAction.HOLD_COHORT,
            {"stability": stability}, []
        )
