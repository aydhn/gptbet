import pytest
from sports_signal_bot.distributed_coordination.snapshots import SnapshotManager
from sports_signal_bot.distributed_coordination.failover import FailoverManager

def test_snapshot_generation_and_consistency():
    mgr = SnapshotManager()

    snap = mgr.build_cluster_snapshot(
        "cluster_1",
        "lineage_1",
        ["node_1"],
        {"partition_0": "broker_1"},
        {"shard_1": "node_1"},
        {"pool_1": 10},
        {"pool_1": 0}
    )

    assert snap.cluster_ref == "cluster_1"
    assert mgr.verify_cluster_snapshot_consistency(snap) is True

    snap.membership.member_nodes = []
    assert mgr.verify_cluster_snapshot_consistency(snap) is False

def test_failover_logic():
    mgr = FailoverManager()

    assert mgr.detect_failover_need("degraded", "node_1") is True
    assert mgr.detect_failover_need("healthy", "node_1") is False

    failover = mgr.initiate_safe_failover("cluster_1", "node_1", "node_2")
    assert failover.status == "failover_in_progress"

    revalidation = mgr.revalidate_post_failover_state(failover, True)
    assert revalidation.status == "revalidation_success"

    revalidation_failed = mgr.revalidate_post_failover_state(failover, False)
    assert revalidation_failed.status == "revalidation_failed"
