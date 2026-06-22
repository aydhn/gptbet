import pytest

from sports_signal_bot.geo_hardening.failover_meshes import (
    add_geo_mesh_edge, add_geo_mesh_node, build_geo_failover_mesh,
    summarize_geo_failover_mesh)
from sports_signal_bot.geo_hardening.geo_nodes import (
    compute_geo_edge_lag, detect_geo_mesh_gaps, verify_geo_node_freshness)


def test_geo_failover_mesh_honesty_set():
    # Geo failover mesh honesty set
    mesh = build_geo_failover_mesh("mesh-1", "bounded_geo_failover_mesh")
    node_a = {"id": "node-1", "last_seen": 1000}
    node_b = {"id": "node-2", "last_seen": 900}
    current_time = 1000

    assert verify_geo_node_freshness(node_a, current_time) is True
    assert verify_geo_node_freshness(node_b, current_time) is False  # stale region

    mesh = add_geo_mesh_node(mesh, node_a["id"])
    mesh = add_geo_mesh_node(mesh, node_b["id"])

    lag = compute_geo_edge_lag(node_a["last_seen"], node_b["last_seen"])
    assert lag == 100

    edges = [{"source": "node-1", "target": "node-2", "status": "active"}]
    gaps = detect_geo_mesh_gaps([node_a, node_b, {"id": "node-3"}], edges)
    assert gaps == ["node-3"]
