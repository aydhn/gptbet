from sports_signal_bot.federated_governance.suspensions import suspend_plane_if_unstable, reduce_plane_autonomy, recover_plane_autonomy_if_safe
from sports_signal_bot.federated_governance.contracts import ControlPlaneRecord, PlanePrecedence, PlaneHealthBand, PlaneTrustBand, DelegationMode, PlaneSuspensionRecord

def test_suspend_plane():
    p1 = ControlPlaneRecord(plane_id="p1", plane_name="Global", plane_family="global", precedence=PlanePrecedence.GLOBAL_GOVERNANCE, health=PlaneHealthBand.UNSTABLE)
    suspension = suspend_plane_if_unstable(p1, "Too many escalations")
    assert suspension is not None
    assert p1.active_status is False

def test_reduce_autonomy():
    p1 = ControlPlaneRecord(plane_id="p1", plane_name="Global", plane_family="global", precedence=PlanePrecedence.GLOBAL_GOVERNANCE, health=PlaneHealthBand.HEALTHY)
    reduction = reduce_plane_autonomy(p1, DelegationMode.BOUNDED_EXECUTION, DelegationMode.ADVISORY_ONLY, "Trust degraded")
    assert reduction.new_mode == DelegationMode.ADVISORY_ONLY

def test_recover_plane():
    p1 = ControlPlaneRecord(plane_id="p1", plane_name="Global", plane_family="global", precedence=PlanePrecedence.GLOBAL_GOVERNANCE, health=PlaneHealthBand.HEALTHY, active_status=False)
    suspension = PlaneSuspensionRecord(suspension_id="s1", plane_id="p1", reason="Old reason", active=True)

    recovered = recover_plane_autonomy_if_safe(p1, suspension)
    assert recovered is True
    assert p1.active_status is True
    assert suspension.active is False
