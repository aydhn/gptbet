from typing import List
from .contracts import (
    TraceRouterFederationRecord,
    TraceFederationLinkRecord,
    FederatedTraceNodeRecord,
    FederatedTraceRouteRecord
)

# Status Taxonomies
STATUS_LINK_CURRENT = "link_current"
STATUS_LINK_CAVEATED = "link_caveated"
STATUS_LINK_REVIEW_ONLY = "link_review_only"
STATUS_LINK_DEGRADED = "link_degraded"
STATUS_LINK_BLOCKED = "link_blocked"
STATUS_LINK_EXPIRED = "link_expired"
STATUS_LINK_SUPERSEDED = "link_superseded"

OUTPUT_FEDERATED_TRACE_CURRENT_WITH_CAPS = "federated_trace_current_with_caps"
OUTPUT_FEDERATED_TRACE_CAVEATED = "federated_trace_caveated"
OUTPUT_FEDERATED_TRACE_REVIEW_ONLY = "federated_trace_review_only"
OUTPUT_FEDERATED_TRACE_DEGRADED = "federated_trace_degraded"
OUTPUT_FEDERATED_TRACE_BLOCKED = "federated_trace_blocked"
OUTPUT_FEDERATED_TRACE_STALE = "federated_trace_stale"

def add_trace_federation_link(federation: TraceRouterFederationRecord, source_ref: str, target_ref: str) -> TraceFederationLinkRecord:
    link_id = f"link_{source_ref}_{target_ref}"
    link = TraceFederationLinkRecord(
        link_id=link_id,
        source_router_ref=source_ref,
        target_router_ref=target_ref,
        status=STATUS_LINK_CURRENT
    )
    federation.active_link_refs.append(link_id)
    return link

def validate_trace_federation_link(link: TraceFederationLinkRecord) -> bool:
    return link.status in [STATUS_LINK_CURRENT, STATUS_LINK_CAVEATED]

def compute_federated_trace_currentness(nodes: List[FederatedTraceNodeRecord]) -> str:
    for node in nodes:
        if node.currentness_state == "stale":
            return "stale"
        if node.currentness_state == "caveated":
            return "caveated"
    return "current"

def summarize_trace_federation_health(federation: TraceRouterFederationRecord) -> str:
    if federation.warnings:
        return "degraded"
    return "healthy"

def aggregate_federated_trace_routes(routes: List[FederatedTraceRouteRecord]) -> str:
    # Rule: stale trace routes cannot be strong federation basis
    stale = any(r.output_scope == OUTPUT_FEDERATED_TRACE_STALE for r in routes)
    if stale:
         return OUTPUT_FEDERATED_TRACE_STALE

    degraded = any(r.output_scope == OUTPUT_FEDERATED_TRACE_DEGRADED for r in routes)
    if degraded:
        return OUTPUT_FEDERATED_TRACE_DEGRADED

    caveated = any(r.output_scope == OUTPUT_FEDERATED_TRACE_CAVEATED for r in routes)
    if caveated:
         return OUTPUT_FEDERATED_TRACE_CAVEATED

    return OUTPUT_FEDERATED_TRACE_CURRENT_WITH_CAPS

def preserve_lineage_and_caveats_in_trace_federation(route: FederatedTraceRouteRecord, caveats: List[str]):
    route.preserved_caveat_refs.extend(caveats)

def preserve_no_safe_trace_paths_in_federation(route: FederatedTraceRouteRecord):
    route.no_safe_visibility_state = "preserved"

def explain_federated_trace_output(route: FederatedTraceRouteRecord) -> str:
    return f"Federated trace output scope is {route.output_scope} with caveats {len(route.preserved_caveat_refs)}"

def enumerate_federated_trace_routes(federation: TraceRouterFederationRecord) -> List[FederatedTraceRouteRecord]:
    return []

def score_federated_trace_routes(routes: List[FederatedTraceRouteRecord]):
    pass

def apply_trace_federation_constraints(routes: List[FederatedTraceRouteRecord]):
    for route in routes:
        if route.warnings:
            route.output_scope = OUTPUT_FEDERATED_TRACE_CAVEATED

def summarize_federated_trace_routes(routes: List[FederatedTraceRouteRecord]) -> str:
    return f"Summarized {len(routes)} routes"
