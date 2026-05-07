from src.sports_signal_bot.planetary_mesh_hardening.bus_meshes import build_planetary_bus_mesh, verify_planetary_bus_mesh
from src.sports_signal_bot.planetary_mesh_hardening.contracts import MeshStatus

def test_planetary_bus_mesh_honesty():
    # 1) Planetary bus mesh honesty set
    mesh = build_planetary_bus_mesh("m_honesty", "bounded_planetary_bus_mesh")
    mesh.packet_refs.append("healthy_packet")
    mesh.edge_refs.append("healthy_edge")

    verify_planetary_bus_mesh(mesh)
    assert mesh.mesh_status == MeshStatus.MESH_VERIFIED

def test_stale_support_corridor_rejection():
    # 2) Stale support corridor rejection set
    mesh = build_planetary_bus_mesh("m_stale", "composite_planetary_bus_mesh")
    mesh.packet_refs.append("stale")

    verify_planetary_bus_mesh(mesh)
    assert mesh.mesh_status == MeshStatus.MESH_CAVEATED
    assert "stale packet support rejected" in mesh.warnings
