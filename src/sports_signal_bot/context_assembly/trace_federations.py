import uuid
from typing import List, Optional
from .contracts import (
    TraceRouterFederationRecord,
    FederatedTraceRouteRecord
)
from .federation_links import aggregate_federated_trace_routes, apply_trace_federation_constraints

def build_trace_router_federation(family: str, policy_ref: str) -> TraceRouterFederationRecord:
    fed_id = f"trf_{uuid.uuid4().hex[:8]}"
    return TraceRouterFederationRecord(
        trace_router_federation_id=fed_id,
        federation_family=family,
        member_trace_router_refs=[],
        active_link_refs=[],
        currentness_policy_ref=policy_ref,
        lineage_policy_ref="lineage_default",
        scope_policy_ref="scope_default",
        health_status="healthy"
    )

def process_trace_federation(federation: TraceRouterFederationRecord, routes: List[FederatedTraceRouteRecord]) -> str:
    # Rules: scope mismatch -> explicit downgrade, sovereignty warnings preserved.
    apply_trace_federation_constraints(routes)
    return aggregate_federated_trace_routes(routes)
