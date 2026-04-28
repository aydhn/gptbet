from sports_signal_bot.approvals.overrides import apply_override_precedence
from sports_signal_bot.approvals.contracts import OverrideRecord, OverrideType, ApprovalScope, OverrideScopeRecord

def test_override_precedence_sorting():
    o1 = OverrideRecord(override_id="o1", override_type=OverrideType.force_stable_only_mode, operator_id="admin1", reason="", scope=OverrideScopeRecord(scope_type=ApprovalScope.system_wide_freeze))
    o2 = OverrideRecord(override_id="o2", override_type=OverrideType.force_freeze, operator_id="admin1", reason="", scope=OverrideScopeRecord(scope_type=ApprovalScope.system_wide_freeze))
    o3 = OverrideRecord(override_id="o3", override_type=OverrideType.suppress_noncritical_alerts, operator_id="admin1", reason="", scope=OverrideScopeRecord(scope_type=ApprovalScope.system_wide_freeze))

    sorted_ovs = apply_override_precedence([o1, o2, o3])
    assert sorted_ovs[0].override_id == "o2" # freeze (100)
    assert sorted_ovs[1].override_id == "o1" # stable (70)
    assert sorted_ovs[2].override_id == "o3" # suppress (30)
