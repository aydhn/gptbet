from typing import Any, Dict, List

from sports_signal_bot.consistency_ledgers.contracts import (
    ConsistencyLedgerEntryRecord,
    ConsistencyShiftFamily,
    ConsistencyShiftRecord,
    ConsistencyState,
    SovereignGovernanceConsistencyLedgerRecord,
)
from sports_signal_bot.consistency_ledgers.utils import generate_id


def compute_consistency_shifts(
    ledger: SovereignGovernanceConsistencyLedgerRecord,
    entry: ConsistencyLedgerEntryRecord,
    previous_state: ConsistencyState,
    new_state: ConsistencyState,
    reason: str,
) -> ConsistencyShiftRecord:

    family = ConsistencyShiftFamily.STABLE_CONSISTENCY
    if previous_state == new_state:
        pass
    elif new_state == ConsistencyState.CONTRADICTED:
        family = ConsistencyShiftFamily.NEWLY_CONTRADICTED
    elif (
        previous_state == ConsistencyState.CONTRADICTED
        and new_state != ConsistencyState.CONTRADICTED
    ):
        family = ConsistencyShiftFamily.CONTRADICTION_RESOLVED
    elif "no_safe" in reason.lower() and "restore" in reason.lower():
        family = ConsistencyShiftFamily.NO_SAFE_VISIBILITY_RESTORED
    elif "degrade" in reason.lower():
        family = ConsistencyShiftFamily.DEGRADED_CONSISTENCY

    shift = ConsistencyShiftRecord(
        shift_id=generate_id("cons_shift"),
        ledger_id=ledger.consistency_ledger_id,
        shift_family=family,
        previous_state=previous_state.value,
        new_state=new_state.value,
        reason=reason,
        warnings=[],
    )

    return shift


def summarize_consistency_shift(shift: ConsistencyShiftRecord) -> Dict[str, Any]:
    return {
        "shift_id": shift.shift_id,
        "family": shift.shift_family.value,
        "transition": f"{shift.previous_state} -> {shift.new_state}",
        "reason": shift.reason,
    }


def explain_consistency_shift(shift: ConsistencyShiftRecord) -> str:
    return f"Consistency shifted to {shift.new_state} due to {shift.reason} (Shift: {shift.shift_family.value})"
