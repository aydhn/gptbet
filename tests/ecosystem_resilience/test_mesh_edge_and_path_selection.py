from sports_signal_bot.ecosystem_resilience.edges import add_mesh_edge
from sports_signal_bot.ecosystem_resilience.paths import score_mesh_paths, select_bounded_mesh_path, enumerate_mesh_paths
from sports_signal_bot.ecosystem_resilience.contracts import MeshEdgeStatus

def test_mesh_edge_and_path_selection():
    e1 = add_mesh_edge("e1", "hub1", "hub2", ["scope1"], [], MeshEdgeStatus.EDGE_ACTIVE)
    e2 = add_mesh_edge("e2", "hub2", "hub3", ["scope1"], ["sov1"], MeshEdgeStatus.EDGE_ACTIVE)

    paths = enumerate_mesh_paths([e1, e2], "hub1", "hub2")
    scored = score_mesh_paths(paths)
    best = select_bounded_mesh_path(scored)

    assert best.path_outcome == "preferred_bounded_path"
