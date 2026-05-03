import pytest
from sports_signal_bot.distributed_coordination.contentions import DistributedContentionManager

def test_cross_node_contentions():
    mgr = DistributedContentionManager()

    cluster_surfaces = {
        "root_closure_pool": ["node_1", "node_2"],
        "cache_layer": ["node_1"]
    }

    contentions = mgr.detect_distributed_contentions("lane_1", "node_1", cluster_surfaces)
    assert len(contentions) == 1
    assert contentions[0].shared_surface == "root_closure_pool"

    contentions.append(contentions[0]) # Add a duplicate to test grouping
    grouped = mgr.correlate_contentions_across_nodes(contentions)
    assert len(grouped["root_closure_pool"]) == 2
