from sports_signal_bot.federated_governance.contracts import ControlPlaneRecord, PlanePrecedence, PlaneHealthBand, PlaneTrustBand
from sports_signal_bot.federated_governance.planes import resolve_plane_precedence, validate_parent_child_governance, block_lower_plane_conflict_with_higher_plane

def test_resolve_plane_precedence():
    p1 = ControlPlaneRecord(plane_id="p1", plane_name="Global", plane_family="global", precedence=PlanePrecedence.GLOBAL_GOVERNANCE)
    p2 = ControlPlaneRecord(plane_id="p2", plane_name="Family", plane_family="family", precedence=PlanePrecedence.FAMILY_DOMAIN)

    # Lower integer value is higher precedence
    winner = resolve_plane_precedence(p1, p2)
    assert winner.plane_id == "p1"

def test_validate_parent_child_governance():
    parent = ControlPlaneRecord(plane_id="parent", plane_name="Global", plane_family="global", precedence=PlanePrecedence.GLOBAL_GOVERNANCE)
    child = ControlPlaneRecord(plane_id="child", plane_name="Family", plane_family="family", precedence=PlanePrecedence.FAMILY_DOMAIN, parent_plane_id="parent")

    assert validate_parent_child_governance(parent, child) is True

    invalid_child = ControlPlaneRecord(plane_id="child2", plane_name="Child", plane_family="family", precedence=PlanePrecedence.GLOBAL_EMERGENCY, parent_plane_id="parent")
    assert validate_parent_child_governance(parent, invalid_child) is False

def test_block_lower_plane_conflict():
    p1 = ControlPlaneRecord(plane_id="p1", plane_name="Global", plane_family="global", precedence=PlanePrecedence.GLOBAL_GOVERNANCE)
    p2 = ControlPlaneRecord(plane_id="p2", plane_name="Family", plane_family="family", precedence=PlanePrecedence.FAMILY_DOMAIN)

    assert block_lower_plane_conflict_with_higher_plane(p2, p1) is True
