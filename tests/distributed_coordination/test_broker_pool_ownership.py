import pytest
from sports_signal_bot.distributed_coordination.broker_pools import BrokerPoolManager
from sports_signal_bot.distributed_coordination.allocations import BrokerAllocationManager

def test_broker_pool_creation():
    pool_mgr = BrokerPoolManager()
    pool = pool_mgr.build_broker_pool("primary_pool", "sticky_owner_allocation", "cautious_failover")

    assert pool.pool_family == "primary_pool"
    assert pool.health_status == "healthy"

    pressure = pool_mgr.summarize_pool_pressure(pool, 100, 20)
    assert pressure["pressure_index"] == 0.2

def test_allocations_and_handoff():
    alloc_mgr = BrokerAllocationManager()

    partitions = alloc_mgr.partition_token_ownership("pool_1", 4)
    assert len(partitions) == 4

    alloc = alloc_mgr.allocate_via_broker_pool("pool_1", "broker_1", "lane_1")
    assert alloc.lane_ref == "lane_1"

    # Handoff should succeed if snapshot is valid
    handoff = alloc_mgr.handoff_broker_ownership_safely("partition_1", "broker_1", "broker_2", True)
    assert handoff.broker_ref == "broker_2"

    # Handoff should fail if snapshot is invalid
    with pytest.raises(RuntimeError):
        alloc_mgr.handoff_broker_ownership_safely("partition_1", "broker_1", "broker_2", False)
