import pytest
from sports_signal_bot.distributed_coordination.fairness import DistributedFairnessManager

def test_distributed_fairness():
    mgr = DistributedFairnessManager()

    fairness = mgr.compute_cluster_fairness("cluster_1", [0.8, 0.9, 0.85])
    assert fairness.score > 0.0 # Score should be high (close to 1) for close values

    pending_times = {"tenant_1_lane": 400.0, "tenant_2_lane": 100.0}
    risks = mgr.detect_cross_shard_starvation(pending_times, 300.0)
    assert len(risks) == 1
    assert risks[0].target_ref == "tenant_1_lane"

    assert mgr.apply_safe_distributed_fairness("tenant_1_lane", risks) is True
    assert mgr.apply_safe_distributed_fairness("tenant_2_lane", risks) is False
