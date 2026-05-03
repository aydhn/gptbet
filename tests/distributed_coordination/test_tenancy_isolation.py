import pytest
from sports_signal_bot.distributed_coordination.tenancy import TenancyIsolationManager

def test_tenancy_isolation():
    mgr = TenancyIsolationManager()

    policy = mgr.build_tenancy_isolation_policy("tenant_1", ["lane_a", "lane_b"])
    assert policy.tenant_or_domain_ref == "tenant_1"

    assert mgr.validate_cross_tenant_requests(policy, "global_rollback_cache") is False
    assert mgr.validate_cross_tenant_requests(policy, "safe_lane") is True

    all_lanes = ["lane_x", "lane_y", "lane_z"]
    mapping = {"lane_x": "tenant_1", "lane_y": "tenant_2", "lane_z": "tenant_1"}

    visible = mgr.segment_runtime_visibility(policy, all_lanes, mapping)
    assert len(visible) == 2
    assert "lane_y" not in visible

    explanation = mgr.explain_isolation_blocks(policy, "root_closure_pool")
    assert "root_closure_pool" in explanation
