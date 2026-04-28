from typing import List, Optional

from sports_signal_bot.release_management.contracts import (
    ChannelStateRecord,
    PromotionGuardRecord,
    PromotionRequestRecord,
    RequestType,
)
from sports_signal_bot.release_management.state import ChannelStateManager


def check_quarantined_block(
    request: PromotionRequestRecord, state_manager: ChannelStateManager
) -> PromotionGuardRecord:
    state = state_manager.get_active_channel_state(request.sport, request.market_type)
    if (
        request.target_chain_group_id
        and request.target_chain_group_id in state.quarantined_artifacts
    ):
        return PromotionGuardRecord(
            guard_name="quarantined_block",
            passed=False,
            reason=f"Chain {request.target_chain_group_id} is quarantined.",
            severity="critical",
        )
    return PromotionGuardRecord(
        guard_name="quarantined_block", passed=True, reason="No quarantine block."
    )


def check_freeze_active(
    request: PromotionRequestRecord, state: ChannelStateRecord
) -> PromotionGuardRecord:
    if request.request_type in [
        RequestType.unfreeze_release_channel,
        RequestType.quarantine_artifact,
        RequestType.rollback_to_previous_stable,
    ]:
        return PromotionGuardRecord(
            guard_name="freeze_active",
            passed=True,
            reason="Action permitted during freeze.",
        )
    if state.frozen_channel_flags.get("system", False):
        return PromotionGuardRecord(
            guard_name="freeze_active",
            passed=False,
            reason="Channel is currently frozen.",
            severity="critical",
        )
    return PromotionGuardRecord(
        guard_name="freeze_active", passed=True, reason="Channel is not frozen."
    )


def check_previous_stable_available(
    request: PromotionRequestRecord, state: ChannelStateRecord
) -> PromotionGuardRecord:
    if request.request_type != RequestType.rollback_to_previous_stable:
        return PromotionGuardRecord(
            guard_name="previous_stable_available",
            passed=True,
            reason="N/A",
        )
    if not state.previous_stable_chain_id:
        return PromotionGuardRecord(
            guard_name="previous_stable_available",
            passed=False,
            reason="No previous stable chain recorded.",
            severity="critical",
        )
    return PromotionGuardRecord(
        guard_name="previous_stable_available",
        passed=True,
        reason="Previous stable chain available.",
    )


def check_missing_canary(
    request: PromotionRequestRecord, state: ChannelStateRecord
) -> PromotionGuardRecord:
    if request.request_type == RequestType.promote_canary_to_stable:
        if not state.active_canary_chain_id:
            return PromotionGuardRecord(
                guard_name="missing_canary",
                passed=False,
                reason="No active canary chain to promote.",
                severity="critical",
            )
        if request.target_chain_group_id and request.target_chain_group_id != state.active_canary_chain_id:
            return PromotionGuardRecord(
                guard_name="missing_canary",
                passed=False,
                reason=f"Target chain {request.target_chain_group_id} does not match active canary {state.active_canary_chain_id}.",
                severity="critical",
            )
    return PromotionGuardRecord(
        guard_name="missing_canary", passed=True, reason="Canary check passed."
    )


def evaluate_all_guards(
    request: PromotionRequestRecord, state_manager: ChannelStateManager
) -> List[PromotionGuardRecord]:
    state = state_manager.get_active_channel_state(request.sport, request.market_type)
    return [
        check_quarantined_block(request, state_manager),
        check_freeze_active(request, state),
        check_previous_stable_available(request, state),
        check_missing_canary(request, state),
    ]
