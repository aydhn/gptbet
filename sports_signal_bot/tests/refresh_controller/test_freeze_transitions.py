import pytest
from sports_signal_bot.refresh_controller.freeze import FreezeManager

def test_activate_freeze():
    mgr = FreezeManager()
    record = mgr.activate_freeze("critical failure")

    assert record.freeze_reason == "critical failure"
    assert record.freeze_scope == "global"
    assert record.active is True

    current = mgr.get_current_freeze()
    assert current is not None
    assert current.freeze_reason == "critical failure"

def test_release_freeze():
    mgr = FreezeManager()
    mgr.activate_freeze("minor issues")
    mgr.release_freeze()

    assert mgr.get_current_freeze() is None
