from typing import Dict, Any
from .base import BaseCohortAutopilotStrategy
from ..contracts import (
    AutopilotDecisionRecord, AutopilotAction, ActivationLevel, AdoptionCohortRecord
)
from ..decisions import create_decision

class NarrowScopeGrowthStrategy(BaseCohortAutopilotStrategy):
    """
    Dar scope cohort'ları nispeten hızlı büyütür.
    Medium/broad scope agresif büyümez.
    """
    def evaluate(self, cohort: AdoptionCohortRecord, context: Dict[str, Any]) -> AutopilotDecisionRecord:
        blockers = context.get("blockers", [])
        stability = context.get("stability_score", 0.0)
        is_narrow = context.get("is_narrow_scope", False)

        if blockers:
            return create_decision(
                cohort.cohort_id, cohort.activation_level, AutopilotAction.PAUSE_COHORT,
                {"stability": stability}, blockers
            )

        if is_narrow and stability >= 0.8:
            return create_decision(
                cohort.cohort_id, cohort.activation_level, AutopilotAction.PROGRESS_COHORT,
                {"stability": stability, "narrow_bonus": 0.2}, []
            )

        return create_decision(
            cohort.cohort_id, cohort.activation_level, AutopilotAction.HOLD_COHORT,
            {"stability": stability}, []
        )
