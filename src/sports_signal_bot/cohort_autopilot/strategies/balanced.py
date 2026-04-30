from typing import Dict, Any
from .base import BaseCohortAutopilotStrategy
from ..contracts import (
    AutopilotDecisionRecord, AutopilotAction, ActivationLevel, AdoptionCohortRecord
)
from ..decisions import create_decision

class BalancedCohortAutopilotStrategy(BaseCohortAutopilotStrategy):
    """
    Clean cohorts controlled grow eder.
    Mixed evidence'ta pause/shrink.
    """
    def evaluate(self, cohort: AdoptionCohortRecord, context: Dict[str, Any]) -> AutopilotDecisionRecord:
        blockers = context.get("blockers", [])
        stability = context.get("stability_score", 0.0)

        if blockers:
            return create_decision(
                cohort.cohort_id, cohort.activation_level, AutopilotAction.PAUSE_COHORT,
                {"stability": stability}, blockers
            )

        if stability >= 0.9:
            next_lvl = ActivationLevel.LEVEL_2_SMALL_COHORT if cohort.activation_level == ActivationLevel.LEVEL_1_NARROW_ACTIVATION else cohort.activation_level
            return create_decision(
                cohort.cohort_id, cohort.activation_level, AutopilotAction.PROGRESS_COHORT,
                {"stability": stability}, [], next_lvl
            )
        elif stability >= 0.7:
            return create_decision(
                cohort.cohort_id, cohort.activation_level, AutopilotAction.SHRINK_COHORT_SCOPE,
                {"stability": stability}, []
            )
        else:
            return create_decision(
                cohort.cohort_id, cohort.activation_level, AutopilotAction.ROLLBACK_COHORT,
                {"stability": stability}, []
            )
