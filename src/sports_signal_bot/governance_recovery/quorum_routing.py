from typing import List, Dict, Any, Optional
from .contracts import (
    QuorumExchangeRoutingFabricRecord,
    QuorumRoutingNodeRecord,
    QuorumRoutingEdgeRecord,
    QuorumRoutingPathRecord,
    QuorumRoutingDecisionRecord,
    QuorumRoutingConstraintRecord,
    QuorumRoutingPressureRecord,
    QuorumRoutingHealthRecord,
    QuorumRoutingManifestRecord,
    QuorumRoutingWarningRecord,
    EdgeStatus,
    RoutingPathOutcome,
    RoutingPressureState
)

def build_quorum_exchange_routing_fabric(fabric_id: str, family: str) -> QuorumExchangeRoutingFabricRecord:
    health = QuorumRoutingHealthRecord(is_healthy=True)
    return QuorumExchangeRoutingFabricRecord(
        quorum_routing_fabric_id=fabric_id,
        fabric_family=family,
        routing_policy_ref="default_routing",
        pressure_policy_ref="default_pressure",
        degradation_policy_ref="default_degradation",
        health_status=health
    )

def add_quorum_routing_node(fabric: QuorumExchangeRoutingFabricRecord, node: QuorumRoutingNodeRecord) -> QuorumExchangeRoutingFabricRecord:
    fabric.node_refs.append(node.node_id)
    return fabric

def add_quorum_routing_edge(fabric: QuorumExchangeRoutingFabricRecord, edge: QuorumRoutingEdgeRecord) -> QuorumExchangeRoutingFabricRecord:
    fabric.edge_refs.append(edge.edge_id)
    return fabric

def validate_quorum_routing_edge(edge: QuorumRoutingEdgeRecord) -> bool:
    if edge.edge_status in [EdgeStatus.ROUTE_EDGE_BLOCKED, EdgeStatus.ROUTE_EDGE_EXPIRED, EdgeStatus.ROUTE_EDGE_SUPERSEDED]:
        return False
    return True

def summarize_quorum_routing_fabric(fabric: QuorumExchangeRoutingFabricRecord) -> QuorumRoutingHealthRecord:
    return fabric.health_status
