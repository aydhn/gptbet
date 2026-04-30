from typing import List, Dict, Any, Tuple
import uuid
from datetime import datetime
from .contracts import ExpansionControlStateRecord, ExpansionStatus

def enter_global_pause(state: ExpansionControlStateRecord, reason: str) -> None:
    """Activates a global pause, halting all new growth."""
    state.global_status = ExpansionStatus.GLOBAL_EMERGENCY_PAUSE
    state.emergency_flags.append(f"GLOBAL_PAUSE: {reason}")
    state.warnings.append(f"[{datetime.utcnow().isoformat()}] Entered Global Pause: {reason}")

def exit_global_pause_if_safe(state: ExpansionControlStateRecord, override: bool = False) -> Tuple[bool, str]:
    """Attempts to lift a global pause, subject to safety checks or manual override."""
    if state.global_status != ExpansionStatus.GLOBAL_EMERGENCY_PAUSE:
        return False, "Not currently in global pause."

    if override:
        state.global_status = ExpansionStatus.EXPANSION_NORMAL
        state.emergency_flags = [f for f in state.emergency_flags if not f.startswith("GLOBAL_PAUSE")]
        state.warnings.append(f"[{datetime.utcnow().isoformat()}] Exited Global Pause via override.")
        return True, "Global pause lifted manually."

    # Auto-unpause is generally prohibited without review in this phase
    return False, "Auto-unpause from global pause is prohibited. Manual override required."

def freeze_family_scope(state: ExpansionControlStateRecord, family_name: str, reason: str) -> None:
    """Freezes progression for a specific family, leaving others unaffected."""
    state.family_freeze_states[family_name] = True
    msg = f"FREEZE_{family_name}: {reason}"
    if msg not in state.emergency_flags:
        state.emergency_flags.append(msg)
    state.warnings.append(f"[{datetime.utcnow().isoformat()}] Family '{family_name}' frozen: {reason}")

    # If not already paused or in a worse state, set to cautious/selective freeze
    if state.global_status in [ExpansionStatus.EXPANSION_NORMAL, ExpansionStatus.EXPANSION_CAUTIOUS]:
        state.global_status = ExpansionStatus.SELECTIVE_FAMILY_FREEZE

def unfreeze_family_scope(state: ExpansionControlStateRecord, family_name: str, override: bool = False) -> Tuple[bool, str]:
    """Lifts a freeze on a specific family."""
    if not state.family_freeze_states.get(family_name, False):
        return False, f"Family '{family_name}' is not frozen."

    if not override:
        return False, "Auto-unfreeze is prohibited. Manual review required."

    state.family_freeze_states[family_name] = False
    state.emergency_flags = [f for f in state.emergency_flags if not f.startswith(f"FREEZE_{family_name}")]
    state.warnings.append(f"[{datetime.utcnow().isoformat()}] Family '{family_name}' unfrozen via override.")

    # If no other families are frozen and we aren't globally paused, revert to normal
    if not any(state.family_freeze_states.values()) and state.global_status == ExpansionStatus.SELECTIVE_FAMILY_FREEZE:
        state.global_status = ExpansionStatus.EXPANSION_NORMAL

    return True, f"Family '{family_name}' freeze lifted."

def summarize_freeze_state(state: ExpansionControlStateRecord) -> Dict[str, Any]:
    """Returns a summary of current freezes and pauses."""
    return {
        "global_status": state.global_status.value,
        "is_globally_paused": state.global_status == ExpansionStatus.GLOBAL_EMERGENCY_PAUSE,
        "frozen_families": [fam for fam, is_frozen in state.family_freeze_states.items() if is_frozen],
        "emergency_flags": state.emergency_flags
    }
