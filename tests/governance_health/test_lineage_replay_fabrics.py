import pytest
from sports_signal_bot.governance_health import (
    build_lineage_replay_fabric,
    add_replay_fabric_node,
    add_replay_fabric_channel,
    validate_replay_fabric_channel,
    summarize_replay_fabric
)

def test_fabric_creation():
    fabric = build_lineage_replay_fabric("exception_lineage_replay_fabric", "p1", "p2")
    assert fabric.fabric_family == "exception_lineage_replay_fabric"

def test_fabric_node_addition():
    fabric = build_lineage_replay_fabric("exception_lineage_replay_fabric", "p1", "p2")
    node = add_replay_fabric_node(fabric, "replay_ingress_node", 100, ["fam1"])
    assert len(fabric.node_refs) == 1
    assert node.replay_capacity == 100

def test_fabric_channel_validation():
    fabric = build_lineage_replay_fabric("exception_lineage_replay_fabric", "p1", "p2")
    n1 = add_replay_fabric_node(fabric, "replay_ingress_node", 100, ["fam1"])
    n2 = add_replay_fabric_node(fabric, "lineage_validation_node", 100, ["fam1"])

    nodes = {n1.node_id: n1, n2.node_id: n2}
    channel = add_replay_fabric_channel(fabric, n1.node_id, n2.node_id, "policy", "policy")

    assert validate_replay_fabric_channel(channel, nodes) is True

    n2.node_status = "inactive"
    assert validate_replay_fabric_channel(channel, nodes) is False
