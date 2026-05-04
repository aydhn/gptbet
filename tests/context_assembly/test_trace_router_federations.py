import pytest
from sports_signal_bot.context_assembly.trace_federations import build_trace_router_federation, process_trace_federation
from sports_signal_bot.context_assembly.federation_links import add_trace_federation_link, validate_trace_federation_link
from sports_signal_bot.context_assembly.contracts import FederatedTraceRouteRecord

def test_build_trace_router_federation():
    fed = build_trace_router_federation("governance_trace_router_federation", "default")
    assert fed.federation_family == "governance_trace_router_federation"
    assert fed.health_status == "healthy"

def test_trace_federation_link():
    fed = build_trace_router_federation("governance_trace_router_federation", "default")
    link = add_trace_federation_link(fed, "src", "tgt")
    assert validate_trace_federation_link(link) is True
    assert link.link_id in fed.active_link_refs

def test_process_trace_federation_stale():
    fed = build_trace_router_federation("governance_trace_router_federation", "default")
    routes = [
        FederatedTraceRouteRecord(
            route_id="r1",
            source_trace_router_refs=[],
            selected_route_refs=[],
            route_currentness_refs=[],
            preserved_caveat_refs=[],
            no_safe_visibility_state="active",
            sovereignty_warning_refs=[],
            output_scope="federated_trace_stale"
        )
    ]
    output = process_trace_federation(fed, routes)
    assert output == "federated_trace_stale"
