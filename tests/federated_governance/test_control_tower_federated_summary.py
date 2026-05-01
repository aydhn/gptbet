from sports_signal_bot.federated_governance.control_tower import FederatedControlTowerBuilder
from sports_signal_bot.federated_governance.contracts import ControlPlaneRecord, PlanePrecedence, PlaneHealthBand, MeshTopologyRecord

def test_build_control_tower_summary():
    p1 = ControlPlaneRecord(plane_id="p1", plane_name="Global", plane_family="global", precedence=PlanePrecedence.GLOBAL_GOVERNANCE, health=PlaneHealthBand.HEALTHY)
    p2 = ControlPlaneRecord(plane_id="p2", plane_name="Family", plane_family="family", precedence=PlanePrecedence.FAMILY_DOMAIN, health=PlaneHealthBand.SUSPENDED, active_status=False)

    topology = MeshTopologyRecord(topology_id="t1", nodes=["p1", "p2"], edges=[])

    builder = FederatedControlTowerBuilder()
    summary = builder.build_summary([p1, p2], [], [], topology, [], [])

    assert summary["governance_topology"]["total_planes"] == 2
    assert summary["governance_topology"]["healthy_planes"] == 1
    assert summary["governance_topology"]["suspended_planes"] == 1
