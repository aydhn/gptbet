from sports_signal_bot.sovereign_mediation.baseline_meshes import build_baseline_federation_mesh, add_baseline_mesh_edge, project_baseline_across_mesh

def test_mesh_projection():
    mesh = build_baseline_federation_mesh("test_family")
    edge = add_baseline_mesh_edge(mesh, "node_a", "node_b")

    assert project_baseline_across_mesh(edge) == "projected_bounded_hint"

    edge.currentness_state = "stale"
    assert project_baseline_across_mesh(edge) == "projected_caveated_hint"
