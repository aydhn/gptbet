import pytest
from sports_signal_bot.refresh_controller.degrade import DegradeManager

def test_activate_degrade():
    mgr = DegradeManager()
    record = mgr.activate_degrade("moderate", "repeated fallbacks")

    assert record.degrade_level == "moderate"
    assert record.reason == "repeated fallbacks"
    assert record.active is True

    current = mgr.get_current_degrade()
    assert current is not None
    assert current.degrade_level == "moderate"

def test_release_degrade():
    mgr = DegradeManager()
    mgr.activate_degrade("mild", "minor issues")
    mgr.release_degrade()

    assert mgr.get_current_degrade() is None
