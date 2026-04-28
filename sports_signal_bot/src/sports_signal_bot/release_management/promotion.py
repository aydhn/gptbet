import uuid
from datetime import datetime, timezone

from sports_signal_bot.core.logger import get_logger
from sports_signal_bot.release_management.channels import ReleaseChannel
from sports_signal_bot.release_management.contracts import (
    PromotionDecisionRecord,
    PromotionPlanRecord,
    PromotionRequestRecord,
)
from sports_signal_bot.release_management.guards import evaluate_all_guards
from sports_signal_bot.release_management.state import ChannelStateManager

logger = get_logger("PromotionEngine")


class PromotionDecisionEngine:
    def __init__(self, state_manager: ChannelStateManager):
        self.state_manager = state_manager

    def evaluate_request(
        self, request: PromotionRequestRecord
    ) -> PromotionDecisionRecord:
        logger.info(f"Evaluating promotion request {request.request_id}")

        guards = evaluate_all_guards(request, self.state_manager)

        decision = "approved"
        rationale = "All guards passed."
        warnings = []

        for guard in guards:
            if not guard.passed:
                if guard.severity == "critical":
                    decision = "rejected"
                    rationale = f"Blocked by guard: {guard.guard_name} - {guard.reason}"
                    break
                else:
                    warnings.append(f"Guard warning: {guard.guard_name} - {guard.reason}")

        # Assume some basic approval logic placeholder
        requires_approval = request.risk_level in ["high", "critical"]

        return PromotionDecisionRecord(
            decision_id=str(uuid.uuid4()),
            request_id=request.request_id,
            decision=decision,
            rationale=rationale,
            guards_evaluated=guards,
            requires_approval=requires_approval,
            approval_status="pending" if requires_approval and decision == "approved" else None,
            warnings=warnings,
        )


class PromotionExecutor:
    def __init__(self, state_manager: ChannelStateManager):
        self.state_manager = state_manager

    def execute_plan(self, plan: PromotionPlanRecord, request: PromotionRequestRecord) -> None:
        logger.info(f"Executing promotion plan {plan.plan_id}")

        for step in plan.steps:
            step.status = "executing"
            try:
                if step.target_channel == ReleaseChannel.stable:
                    self.state_manager.promote_channel_pointer(
                        request.sport, request.market_type, "stable", step.target_chain_group_id
                    )
                elif step.target_channel == ReleaseChannel.canary:
                    self.state_manager.promote_channel_pointer(
                        request.sport, request.market_type, "canary", step.target_chain_group_id
                    )
                elif step.target_channel == ReleaseChannel.quarantined:
                    if step.target_artifact_id:
                        self.state_manager.mark_artifact_quarantined(
                            request.sport, request.market_type, step.target_artifact_id
                        )
                    elif step.target_chain_group_id:
                        self.state_manager.mark_artifact_quarantined(
                            request.sport, request.market_type, step.target_chain_group_id
                        )

                step.status = "success"
                step.execution_time = datetime.now(timezone.utc)
            except Exception as e:
                step.status = "failed"
                step.error = str(e)
                logger.error(f"Step {step.step_id} failed: {e}")

        plan.status = "completed" if all(s.status == "success" for s in plan.steps) else "failed"
