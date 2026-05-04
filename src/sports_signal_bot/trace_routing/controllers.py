from typing import List, Dict, Any, Optional

from .contracts import (
    ProofCatalogFederationRecord,
    ObservatorySignalExchangeRecord,
    NarrativeIntegrityCouncilRecord,
    SovereignGovernanceTraceRouterRecord,
    TraceRoutingSummary
)

from .proof_federations import summarize_proof_federation_health
from .signal_exchanges import summarize_observatory_signal_exchange
from .integrity_councils import summarize_narrative_integrity_council
from .trace_routers import summarize_trace_router_health

class TraceRoutingController:
    def __init__(self):
        self.federations = []
        self.exchanges = []
        self.councils = []
        self.routers = []

    def run_trace_routing_pass(self) -> TraceRoutingSummary:
        summary = TraceRoutingSummary()
        summary.overall_health = "healthy"

        for fed in self.federations:
            health = summarize_proof_federation_health(fed)
            summary.proof_federation_counts_by_health[health] = summary.proof_federation_counts_by_health.get(health, 0) + 1

        for exch in self.exchanges:
            status = exch.exchange_status.value
            summary.signal_exchange_counts[status] = summary.signal_exchange_counts.get(status, 0) + 1

        for council in self.councils:
            health = council.health_status
            summary.narrative_integrity_counts[health] = summary.narrative_integrity_counts.get(health, 0) + 1

        for router in self.routers:
            health = summarize_trace_router_health(router)
            summary.trace_router_route_counts[health] = summary.trace_router_route_counts.get(health, 0) + 1

        return summary
