from sports_signal_bot.governance_recovery.quorum_routing import (
    build_quorum_exchange_routing_fabric,
    validate_quorum_routing_edge
)
from sports_signal_bot.governance_recovery.contracts import QuorumRoutingEdgeRecord, EdgeStatus

def test_build_quorum_exchange_routing_fabric():
    fabric = build_quorum_exchange_routing_fabric("fab_1", "bounded_governance_quorum_routing_fabric")
    assert fabric.quorum_routing_fabric_id == "fab_1"
    assert fabric.health_status.is_healthy is True

def test_validate_quorum_routing_edge():
    edge = QuorumRoutingEdgeRecord(
        edge_id="e1", source_node_ref="n1", target_node_ref="n2", currentness_state="current", caveat_transfer_policy="keep", edge_status=EdgeStatus.ROUTE_EDGE_CURRENT
    )
    assert validate_quorum_routing_edge(edge) is True

    blocked_edge = QuorumRoutingEdgeRecord(
        edge_id="e2", source_node_ref="n1", target_node_ref="n2", currentness_state="stale", caveat_transfer_policy="keep", edge_status=EdgeStatus.ROUTE_EDGE_BLOCKED
    )
    assert validate_quorum_routing_edge(blocked_edge) is False
