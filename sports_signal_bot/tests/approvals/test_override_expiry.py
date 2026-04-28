from sports_signal_bot.approvals.overrides import OverrideManager
from sports_signal_bot.approvals.contracts import OverrideRecord, OverrideType, ApprovalScope, OverrideScopeRecord
from datetime import datetime, timezone, timedelta

def test_override_expiry_filtering():
    manager = OverrideManager()
    now = datetime.now(timezone.utc)

    # Active
    manager.add_override(OverrideRecord(override_id="o1", override_type=OverrideType.force_freeze, operator_id="op1", reason="", scope=OverrideScopeRecord(scope_type=ApprovalScope.system_wide_freeze)))

    # Expired
    manager.add_override(OverrideRecord(override_id="o2", override_type=OverrideType.force_freeze, operator_id="op1", reason="", expires_at=now - timedelta(hours=1), scope=OverrideScopeRecord(scope_type=ApprovalScope.system_wide_freeze)))

    active = manager.get_active_overrides()
    assert len(active) == 1
    assert active[0].override_id == "o1"

    # Check that status was updated
    expired = manager.get_override("o2")
    assert expired.status == "expired"
