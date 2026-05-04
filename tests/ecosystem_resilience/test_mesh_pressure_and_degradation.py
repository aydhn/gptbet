from sports_signal_bot.ecosystem_resilience.meshes import compute_mesh_health, build_hub_routing_mesh
from sports_signal_bot.ecosystem_resilience.contracts import MeshPressureOutcome, MeshEdgeStatus
from sports_signal_bot.ecosystem_resilience.edges import add_mesh_edge

def test_mesh_pressure_and_degradation():
    mesh = build_hub_routing_mesh("m1", "internal", ["hub1"], ["e1"], "pol1", MeshPressureOutcome.HIGH_PRESSURE)
    e1 = add_mesh_edge("e1", "hub1", "hub2", ["scope1"], [], MeshEdgeStatus.EDGE_DEGRADED)

    health = compute_mesh_health(mesh, [e1])
    assert health == "critical"
