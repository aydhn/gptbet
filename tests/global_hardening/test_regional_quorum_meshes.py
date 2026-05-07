from sports_signal_bot.global_hardening.contracts import RegionalQuorumMeshRecord, QuorumMeshNodeRecord
from sports_signal_bot.global_hardening.quorum_meshes import build_regional_quorum_mesh, add_quorum_mesh_node

def test_stale_region_rejection():
    mesh = build_regional_quorum_mesh("m1", "bounded_regional_quorum_mesh")
    node1 = QuorumMeshNodeRecord(node_id="n1", node_family="primary", region="r1", status="stale")
    add_quorum_mesh_node(mesh, node1)

    assert mesh.mesh_status == "mesh_blocked"
    assert len(mesh.warnings) > 0
