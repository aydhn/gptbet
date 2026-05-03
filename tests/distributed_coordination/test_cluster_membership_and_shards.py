import pytest
from sports_signal_bot.distributed_coordination.clusters import CoordinationClusterManager
from sports_signal_bot.distributed_coordination.nodes import CoordinationNodeManager
from sports_signal_bot.distributed_coordination.shards import SchedulerShardManager

def test_cluster_creation_and_membership():
    cluster_mgr = CoordinationClusterManager()
    node_mgr = CoordinationNodeManager()

    cluster = cluster_mgr.build_cluster("test_cluster", "local_coordination_cluster", "policy_1")
    assert cluster.cluster_name == "test_cluster"
    assert cluster.active_status == "active"

    node = node_mgr.build_node(cluster.cluster_id, ["scheduler_node", "broker_node"])
    assert "scheduler_node" in node.roles
    assert node.active is True

    membership = cluster_mgr.join_cluster(cluster.cluster_id, node.node_id)
    assert membership.status == "active"
    assert membership.node_ref == node.node_id

def test_scheduler_shards():
    shard_mgr = SchedulerShardManager()
    shards = shard_mgr.build_scheduler_shards("tenant_shard", 3, "node_1")

    assert len(shards) == 3
    assert shards[0].shard_family == "tenant_shard"

    # Test load balancing
    shards[0].load = 10.0
    shards[1].load = 5.0
    shards[2].load = 15.0

    assigned = shard_mgr.assign_lane_to_shard("lane_1", shards)
    assert assigned.shard_id == shards[1].shard_id

    # Test cross shard conflict
    assignments = {"lane_2": shards[0].shard_id}
    conflict = shard_mgr.detect_cross_shard_conflicts("lane_2", assignments)
    assert conflict is True
