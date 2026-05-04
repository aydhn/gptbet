import pytest
from src.sports_signal_bot.trace_routing.contracts import (
    TraceRouterFamily,
    NodeFamily,
    EdgeRelationshipFamily,
    TraceRouterHealthStatus,
    TracePacketRecord
)
from src.sports_signal_bot.trace_routing.trace_routers import (
    build_governance_trace_router,
    add_trace_router_node,
    add_trace_router_edge,
    build_trace_packet
)

def test_build_governance_trace_router():
    router = build_governance_trace_router(
        TraceRouterFamily.GOVERNANCE_TRACE_ROUTER,
        "rout_pol", "const_pol", "drill_pol"
    )
    assert router.health_status == TraceRouterHealthStatus.HEALTHY

def test_add_trace_router_node():
    router = build_governance_trace_router(
        TraceRouterFamily.GOVERNANCE_TRACE_ROUTER,
        "rout_pol", "const_pol", "drill_pol"
    )
    node = add_trace_router_node(
        router, NodeFamily.PROOF_NODE, "src1", "fam1", "current", "clean"
    )
    assert node.node_id in router.node_refs

def test_build_trace_packet():
    packet = build_trace_packet("orig", "scope", "visible")
    assert packet.output_scope == "scope"
