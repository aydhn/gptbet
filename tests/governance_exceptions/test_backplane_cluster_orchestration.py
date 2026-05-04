import pytest
from sports_signal_bot.governance_exceptions.contracts import BackplaneClusterRecord, BackplaneClusterNodeRecord
from sports_signal_bot.governance_exceptions.clusters import build_backplane_cluster, register_backplane_cluster_node

def test_build_backplane_cluster():
    cluster = build_backplane_cluster("governance_signal_cluster", "policy_1", "policy_2")
    assert cluster.cluster_family == "governance_signal_cluster"
    assert cluster.health_status == "cluster_healthy"

def test_register_backplane_cluster_node():
    cluster = build_backplane_cluster("governance_signal_cluster", "policy_1", "policy_2")
    node = BackplaneClusterNodeRecord(
        node_id="node_1",
        node_family="ingress_node",
        hosted_segment_refs=[],
        hosted_channel_refs=[],
        pressure_state="low",
        freshness_state="fresh",
        replay_load=10.0,
        node_status="active",
        warnings=[]
    )
    register_backplane_cluster_node(cluster, node)
    assert "node_1" in cluster.node_refs
