from datetime import datetime
from typing import List, Dict, Optional
from sports_signal_bot.corridor_governance.contracts import (
    TreatyLifecycleStateRecord,
    TreatyLifecycleControllerRecord,
    TreatyLifecycleTransitionRecord
)

def build_treaty_lifecycle_controller(states: List[TreatyLifecycleStateRecord]) -> TreatyLifecycleControllerRecord:
    return TreatyLifecycleControllerRecord(states=states)

def evaluate_treaty_transition(
    current_state: TreatyLifecycleStateRecord,
    target_state_name: str
) -> bool:
    # Allowed transitions logic
    allowed = {
        "treaty_drafted": ["treaty_reviewing"],
        "treaty_reviewing": ["treaty_active"],
        "treaty_active": ["treaty_active_caution", "treaty_renewal_due", "treaty_expired", "treaty_superseded", "treaty_suspended", "treaty_terminated"],
        "treaty_active_caution": ["treaty_renewal_due", "treaty_expired", "treaty_superseded", "treaty_suspended", "treaty_terminated"],
        "treaty_renewal_due": ["treaty_active", "treaty_expired", "treaty_superseded"],
        "treaty_suspended": ["treaty_active", "treaty_terminated"],
        "treaty_expired": [],
        "treaty_superseded": [],
        "treaty_terminated": []
    }
    return target_state_name in allowed.get(current_state.lifecycle_state, [])

def apply_treaty_transition(
    current_state: TreatyLifecycleStateRecord,
    target_state_name: str,
    transition_time: datetime
) -> TreatyLifecycleTransitionRecord:
    if not evaluate_treaty_transition(current_state, target_state_name):
        raise ValueError(f"Invalid transition from {current_state.lifecycle_state} to {target_state_name}")

    return TreatyLifecycleTransitionRecord(
        treaty_ref=current_state.treaty_ref,
        from_state=current_state.lifecycle_state,
        to_state=target_state_name,
        transition_time=transition_time
    )

def summarize_treaty_lifecycle(controller: TreatyLifecycleControllerRecord) -> Dict[str, int]:
    summary = {}
    for state in controller.states:
        summary[state.lifecycle_state] = summary.get(state.lifecycle_state, 0) + 1
    return summary
