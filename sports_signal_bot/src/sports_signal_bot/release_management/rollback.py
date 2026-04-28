import uuid
from typing import Optional

from sports_signal_bot.core.logger import get_logger
from sports_signal_bot.release_management.contracts import (
    RollbackDecisionRecord,
    RollbackExecutionRecord,
    RollbackPlanRecord,
    RollbackTargetRecord,
    RollbackValidationRecord,
)
from sports_signal_bot.release_management.state import ChannelStateManager

logger = get_logger("RollbackExecutor")


class RollbackPlanner:
    def __init__(self, state_manager: ChannelStateManager):
        self.state_manager = state_manager

    def create_rollback_plan(
        self, sport: str, market_type: str, reason: str
    ) -> Optional[RollbackPlanRecord]:
        state = self.state_manager.get_active_channel_state(sport, market_type)

        if not state.previous_stable_chain_id:
            logger.error("Cannot create rollback plan: No previous stable chain.")
            return None

        # Determine target
        target_id = state.previous_stable_chain_id
        is_quarantined = target_id in state.quarantined_artifacts

        validation = RollbackValidationRecord(
            target_valid=not is_quarantined,
            checks_passed=["target_exists"] if not is_quarantined else [],
            checks_failed=["target_quarantined"] if is_quarantined else [],
        )

        target = RollbackTargetRecord(
            chain_group_id=target_id,
            reason="Revert to previous stable",
            known_safe=not is_quarantined,
        )

        plan = RollbackPlanRecord(
            plan_id=str(uuid.uuid4()),
            sport=sport,
            market_type=market_type,
            source_chain_group_id=state.active_stable_chain_id or "unknown",
            target=target,
            approval_required=False,
            validation=validation,
        )

        return plan


class RollbackExecutor:
    def __init__(self, state_manager: ChannelStateManager):
        self.state_manager = state_manager

    def execute_rollback(self, plan: RollbackPlanRecord) -> RollbackExecutionRecord:
        logger.info(f"Executing rollback plan {plan.plan_id}")

        execution = RollbackExecutionRecord(
            execution_id=str(uuid.uuid4()),
            plan_id=plan.plan_id,
            status="failed",
            log=[],
        )

        if not plan.validation.target_valid:
            execution.log.append("Rollback failed: target is invalid or quarantined.")
            return execution

        # execute pointer swap
        state = self.state_manager.get_active_channel_state(
            plan.sport, plan.market_type
        )

        # we move active to rolled_back essentially (though we don't have a distinct list for it yet)
        state.active_stable_chain_id = plan.target.chain_group_id
        # we don't update previous_stable so we can potentially rollback again if needed? Or we clear it.
        # usually rollback is a one-step undo.

        self.state_manager.set_channel_state(state)

        execution.status = "success"
        execution.log.append(f"Successfully rolled back to {plan.target.chain_group_id}")
        return execution
