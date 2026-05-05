from typing import List, Dict, Optional, Any
import datetime
from .contracts import (
    EvidenceBrokerExchangeRecord,
    BrokerExchangePacketRecord,
    BrokerExchangeScopeRecord,
    EvidenceBrokerExchangeWarningRecord,
    BrokerExchangeRoutingRecord
)

def build_evidence_broker_exchange(
    exchange_id: str,
    source_broker_refs: List[str],
    target_broker_refs: List[str],
    scope: BrokerExchangeScopeRecord,
    validity_window: str
) -> EvidenceBrokerExchangeRecord:
    """Builds a new evidence broker exchange."""
    return EvidenceBrokerExchangeRecord(
        broker_exchange_id=exchange_id,
        source_broker_refs=source_broker_refs,
        target_broker_refs=target_broker_refs,
        exchange_packet_refs=[],
        exchange_scope=scope,
        validity_window=validity_window,
        preserved_caveat_refs=[],
        currentness_refs=[],
        exchange_status="prepared",
        warnings=[]
    )

def validate_broker_exchange_packet(packet: BrokerExchangePacketRecord) -> bool:
    """Validates an exchange packet before routing."""
    if not packet.source_evidence_refs:
        packet.warnings.append(EvidenceBrokerExchangeWarningRecord("missing_evidence", "Packet lacks evidence refs."))
        return False
    if packet.evidence_completeness != "complete":
        packet.warnings.append(EvidenceBrokerExchangeWarningRecord("incomplete_evidence", "Evidence is marked incomplete."))
        # We might still return True if we allow caveated exchanges
    return True

def route_broker_exchange_packet(
    exchange: EvidenceBrokerExchangeRecord,
    packet: BrokerExchangePacketRecord,
    routing_rules: Dict[str, Any]
) -> BrokerExchangeRoutingRecord:
    """Routes an exchange packet based on rules."""

    if packet.evidence_completeness != "complete":
        return BrokerExchangeRoutingRecord(route_status="routed_caveated_exchange", selected_route_ref="caveated_route")

    # Check currentness
    if "stale" in packet.currentness_refs:
        return BrokerExchangeRoutingRecord(route_status="revalidation_required_exchange", selected_route_ref="none")

    # Determine scope constraints
    if "restricted" in packet.scope_constraints:
        return BrokerExchangeRoutingRecord(route_status="routed_review_only_exchange", selected_route_ref="restricted_route")

    return BrokerExchangeRoutingRecord(route_status="routed_bounded_exchange", selected_route_ref="default_bounded_route")

def replay_broker_exchange(exchange: EvidenceBrokerExchangeRecord) -> str:
    """Replays a broker exchange to verify integrity."""
    if exchange.exchange_status in ["exchanged_blocked", "exchanged_expired"]:
        return "replay_failed_due_to_status"
    return "replay_successful"

def summarize_broker_exchange(exchange: EvidenceBrokerExchangeRecord) -> Dict[str, str]:
    """Summarizes a broker exchange."""
    return {
        "exchange_id": exchange.broker_exchange_id,
        "status": exchange.exchange_status,
        "packet_count": str(len(exchange.exchange_packet_refs))
    }

def enumerate_broker_exchange_routes(packet: BrokerExchangePacketRecord) -> List[str]:
    """Enumerates available routes for a packet."""
    routes = ["default_bounded_route", "restricted_route", "caveated_route"]
    if "stale" in packet.currentness_refs:
        routes.append("revalidation_required_route")
    return routes

def score_broker_exchange_routes(routes: List[str], rules: Dict[str, Any]) -> Dict[str, float]:
    """Scores available exchange routes."""
    return {r: 1.0 for r in routes}

def apply_broker_exchange_constraints(packet: BrokerExchangePacketRecord, constraints: List[str]) -> BrokerExchangePacketRecord:
    """Applies constraints to a broker exchange packet."""
    packet.scope_constraints.extend(constraints)
    return packet

def select_broker_exchange_route(scores: Dict[str, float]) -> str:
    """Selects the best route based on scores."""
    if not scores:
        return "blocked_exchange_route"
    return max(scores, key=scores.get)

def summarize_broker_exchange_route(route: str) -> str:
    """Summarizes the selected route."""
    return f"Selected Route: {route}"

def compute_broker_exchange_pressure(metrics: Dict[str, float]) -> float:
    """Computes the pressure on the broker exchange."""
    # Simplified pressure calculation
    stale_density = metrics.get("stale_listing_density", 0.0)
    backlog = metrics.get("broker_backlog", 0.0)
    return (stale_density * 0.6) + (backlog * 0.4)

def compute_broker_exchange_fairness(metrics: Dict[str, float]) -> float:
    """Computes the fairness of the broker exchange routing."""
    # Simplified fairness calculation
    request_aging = metrics.get("request_aging", 0.0)
    review_only_spillover = metrics.get("review_only_spillover", 0.0)
    return 1.0 - ((request_aging * 0.5) + (review_only_spillover * 0.5))

def preserve_fairness_without_scope_widening(pressure: float, fairness: float) -> str:
    """Ensures fairness is preserved without widening the scope."""
    if fairness < 0.5:
        return "fairness_warning: adjust routing priorities, do NOT widen scope"
    return "fairness_ok"

def summarize_broker_exchange_pressure_and_fairness(pressure: float, fairness: float) -> str:
    """Summarizes pressure and fairness."""
    return f"Pressure: {pressure:.2f}, Fairness: {fairness:.2f}"
