import uuid
from typing import Optional

from sports_signal_bot.core.logger import get_logger
from sports_signal_bot.release_management.contracts import (
    PromotionDecisionRecord,
    PromotionPlanRecord,
    PromotionRequestRecord,
    PromotionStepRecord,
    RequestType,
)

logger = get_logger("PromotionPlanner")


class PromotionPlanner:
    def create_plan(
        self, request: PromotionRequestRecord, decision: PromotionDecisionRecord
    ) -> Optional[PromotionPlanRecord]:
        if decision.decision != "approved":
            logger.info("Cannot create plan for non-approved decision.")
            return None

        plan = PromotionPlanRecord(
            plan_id=str(uuid.uuid4()), decision_id=decision.decision_id, steps=[]
        )

        step = PromotionStepRecord(
            step_id=str(uuid.uuid4()),
            action=request.request_type.value,
            target_chain_group_id=request.target_chain_group_id,
            target_artifact_id=request.target_artifact_id,
            target_channel=self._determine_target_channel(request.request_type),
        )
        plan.steps.append(step)

        return plan

    def _determine_target_channel(self, request_type: RequestType):
        from sports_signal_bot.release_management.channels import ReleaseChannel

        if request_type == RequestType.promote_candidate_to_canary:
            return ReleaseChannel.canary
        elif request_type in [
            RequestType.promote_canary_to_stable,
            RequestType.promote_candidate_to_stable_direct,
            RequestType.promote_stable_fallback_chain,
            RequestType.rollback_to_previous_stable,
        ]:
            return ReleaseChannel.stable
        elif request_type == RequestType.quarantine_artifact:
            return ReleaseChannel.quarantined
        return ReleaseChannel.draft
