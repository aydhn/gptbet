import pytest
from sports_signal_bot.geo_hardening.failover_meshes import build_geo_failover_mesh, add_geo_mesh_node, add_geo_mesh_edge, summarize_geo_failover_mesh, verify_geo_mesh_path
from sports_signal_bot.geo_hardening.geo_nodes import verify_geo_node_freshness, compute_geo_edge_lag, detect_geo_mesh_gaps

def test_geo_failover_mesh_honesty_set():
    # Geo failover mesh honesty set
    mesh = build_geo_failover_mesh("mesh-1", "bounded_geo_failover_mesh")
    node_a = {"id": "node-1", "last_seen": 1000}
    node_b = {"id": "node-2", "last_seen": 900}
    current_time = 1000

    assert verify_geo_node_freshness(node_a, current_time) is True
    assert verify_geo_node_freshness(node_b, current_time) is False # stale region

    mesh = add_geo_mesh_node(mesh, node_a["id"])
    mesh = add_geo_mesh_node(mesh, node_b["id"])

    lag = compute_geo_edge_lag(node_a["last_seen"], node_b["last_seen"])
    assert lag == 100

    edges = [{"source": "node-1", "target": "node-2", "status": "active"}]
    gaps = detect_geo_mesh_gaps([node_a, node_b, {"id": "node-3"}], edges)
    assert gaps == ["node-3"]

def test_build_geo_failover_mesh():
    mesh = build_geo_failover_mesh("mesh-2", "family-1")
    assert mesh.geo_failover_mesh_id == "mesh-2"
    assert mesh.mesh_family == "family-1"
    assert mesh.mesh_status == "mesh_ready"

def test_add_geo_mesh_edge():
    mesh = build_geo_failover_mesh("mesh-3", "family-2")
    mesh = add_geo_mesh_edge(mesh, "edge-1")
    assert "edge-1" in mesh.edge_refs

def test_verify_geo_mesh_path():
    mesh = build_geo_failover_mesh("mesh-4", "family-3")
    result = verify_geo_mesh_path(mesh, "path-1")
    assert result is True
    assert "path-1" in mesh.path_refs

def test_summarize_geo_failover_mesh():
    mesh = build_geo_failover_mesh("mesh-5", "family-4")
    mesh = add_geo_mesh_node(mesh, "node-1")
    mesh = add_geo_mesh_edge(mesh, "edge-1")
    summary = summarize_geo_failover_mesh(mesh)
    assert summary["mesh_id"] == "mesh-5"
    assert summary["status"] == "mesh_ready"
    assert summary["nodes"] == 1
    assert summary["edges"] == 1
