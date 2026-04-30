import pytest
from sports_signal_bot.expansion_governance.freezes import (
    enter_global_pause, exit_global_pause_if_safe,
    freeze_family_scope, unfreeze_family_scope
)
from sports_signal_bot.expansion_governance.contracts import ExpansionControlStateRecord, ExpansionStatus

def test_global_pause():
    state = ExpansionControlStateRecord(control_state_id="test")
    enter_global_pause(state, "Critical failure")
    assert state.global_status == ExpansionStatus.GLOBAL_EMERGENCY_PAUSE

    success, msg = exit_global_pause_if_safe(state, override=False)
    assert success is False
    assert state.global_status == ExpansionStatus.GLOBAL_EMERGENCY_PAUSE

    success, msg = exit_global_pause_if_safe(state, override=True)
    assert success is True
    assert state.global_status == ExpansionStatus.EXPANSION_NORMAL

def test_family_freeze():
    state = ExpansionControlStateRecord(control_state_id="test")
    freeze_family_scope(state, "alias_memory", "Too many disputes")

    assert state.family_freeze_states["alias_memory"] is True
    assert state.global_status == ExpansionStatus.SELECTIVE_FAMILY_FREEZE

    success, msg = unfreeze_family_scope(state, "alias_memory", override=True)
    assert success is True
    assert state.family_freeze_states["alias_memory"] is False
    assert state.global_status == ExpansionStatus.EXPANSION_NORMAL
