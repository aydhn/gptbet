from sports_signal_bot.federated_governance.overrides import issue_emergency_override, expire_emergency_override, enforce_override_precedence, explain_override_effect_on_planes
from sports_signal_bot.federated_governance.contracts import ControlPlaneRecord, PlanePrecedence

def test_issue_and_expire_override():
    override = issue_emergency_override("global_plane", "family_plane", "pause", "Emergency issue")
    assert override.active is True
    assert override.target_plane_id == "family_plane"

    expiry = expire_emergency_override(override)
    assert override.active is False

def test_enforce_override_precedence():
    override = issue_emergency_override("global_plane", "family_plane", "pause", "Emergency issue")
    p1 = ControlPlaneRecord(plane_id="family_plane", plane_name="Family", plane_family="family", precedence=PlanePrecedence.FAMILY_DOMAIN)
    p2 = ControlPlaneRecord(plane_id="other_plane", plane_name="Other", plane_family="family", precedence=PlanePrecedence.FAMILY_DOMAIN)

    assert enforce_override_precedence(override, p1) is True
    assert enforce_override_precedence(override, p2) is False

    # Test global override (target=None)
    override_global = issue_emergency_override("global_plane", None, "pause", "Global emergency")
    assert enforce_override_precedence(override_global, p2) is True
