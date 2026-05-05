import uuid
from typing import List, Dict, Any
from .contracts import (
    TraceEvidenceBrokerRecord,
    EvidenceBrokerListingRecord,
    EvidenceBrokerRequestRecord,
    EvidenceBrokerMatchRecord
)

# EVIDENCE BROKER FAMILY TAXONOMY
INTERNAL_TRACE_EVIDENCE_BROKER = "internal_trace_evidence_broker"
REVIEW_ONLY_EVIDENCE_BROKER = "review_only_evidence_broker"
BOUNDED_TRACE_EVIDENCE_BROKER = "bounded_trace_evidence_broker"
PROOF_SUPPORT_EVIDENCE_BROKER = "proof_support_evidence_broker"
CONTEXT_BUNDLE_EVIDENCE_BROKER = "context_bundle_evidence_broker"
DEGRADED_EVIDENCE_BROKER = "degraded_evidence_broker"
SOVEREIGNTY_WARNING_EVIDENCE_BROKER = "sovereignty_warning_evidence_broker"

# LISTING STATUS TAXONOMY
LISTED_CURRENT = "listed_current"
LISTED_CAVEATED = "listed_caveated"
LISTED_REVIEW_ONLY = "listed_review_only"
LISTED_BACKPRESSURED = "listed_backpressured"
LISTED_DEGRADED = "listed_degraded"
LISTED_MATCHED = "listed_matched"
LISTED_EXPIRED = "listed_expired"
LISTED_SUPERSEDED = "listed_superseded"
LISTED_BLOCKED = "listed_blocked"

# REQUEST STATUS TAXONOMY
REQUEST_OPEN = "request_open"
REQUEST_CAVEATED = "request_caveated"
REQUEST_REVIEW_ONLY = "request_review_only"
REQUEST_BACKPRESSURED = "request_backpressured"
REQUEST_MATCHED = "request_matched"
REQUEST_EXPIRED = "request_expired"
REQUEST_BLOCKED = "request_blocked"

# BROKER MATCH OUTCOME TAXONOMY
MATCHED_BOUNDED_EVIDENCE_ROUTE = "matched_bounded_evidence_route"
MATCHED_REVIEW_ONLY_EVIDENCE_ROUTE = "matched_review_only_evidence_route"
MATCHED_CAVEATED_EVIDENCE_ROUTE = "matched_caveated_evidence_route"
MATCHED_DEGRADED_EVIDENCE_ROUTE = "matched_degraded_evidence_route"
REVALIDATION_REQUIRED_ROUTE = "revalidation_required_route"
BROKER_MATCH_BLOCKED = "broker_match_blocked"
NO_SAFE_EVIDENCE_ROUTE = "no_safe_evidence_route"


def build_trace_evidence_broker(family: str, policies: Dict[str, str]) -> TraceEvidenceBrokerRecord:
    return TraceEvidenceBrokerRecord(
        evidence_broker_id=str(uuid.uuid4()),
        broker_family=family,
        routing_policy_ref=policies.get('routing', 'default'),
        fairness_policy_ref=policies.get('fairness', 'default'),
        ceiling_policy_ref=policies.get('ceiling', 'default'),
        health_status="active"
    )

def create_evidence_broker_listing(broker: TraceEvidenceBrokerRecord, family: str) -> EvidenceBrokerListingRecord:
    listing = EvidenceBrokerListingRecord(
        listing_id=str(uuid.uuid4()),
        listing_family=family,
        source_ref="test_source",
        source_family="test_source_family",
        evidence_completeness="full",
        currentness_state="fresh",
        listing_status=LISTED_CURRENT
    )
    broker.active_listing_refs.append(listing.listing_id)
    return listing

def create_evidence_broker_request(broker: TraceEvidenceBrokerRecord) -> EvidenceBrokerRequestRecord:
    request = EvidenceBrokerRequestRecord(
        request_id=str(uuid.uuid4()),
        status=REQUEST_OPEN
    )
    broker.active_request_refs.append(request.request_id)
    return request

def validate_evidence_broker_compatibility(listing: EvidenceBrokerListingRecord, request: EvidenceBrokerRequestRecord) -> bool:
    if listing.listing_status in [LISTED_BLOCKED, LISTED_EXPIRED]:
        return False
    return True

def summarize_trace_evidence_broker(broker: TraceEvidenceBrokerRecord) -> Dict[str, Any]:
    return {
        "id": broker.evidence_broker_id,
        "listings": len(broker.active_listing_refs),
        "requests": len(broker.active_request_refs),
        "matches": len(broker.active_match_refs),
        "status": broker.health_status
    }

def enumerate_broker_matches(broker: TraceEvidenceBrokerRecord) -> List[EvidenceBrokerMatchRecord]:
    return []

def score_broker_matches(matches: List[EvidenceBrokerMatchRecord]) -> None:
    pass

def apply_broker_constraints(match: EvidenceBrokerMatchRecord) -> None:
    pass

def select_broker_match(listing: EvidenceBrokerListingRecord, request: EvidenceBrokerRequestRecord) -> EvidenceBrokerMatchRecord:
    outcome = MATCHED_BOUNDED_EVIDENCE_ROUTE
    if listing.currentness_state == "stale":
        outcome = MATCHED_DEGRADED_EVIDENCE_ROUTE
    elif listing.evidence_completeness == "partial":
        outcome = MATCHED_CAVEATED_EVIDENCE_ROUTE
    return EvidenceBrokerMatchRecord(
        match_id=str(uuid.uuid4()),
        outcome=outcome
    )

def summarize_broker_match(match: EvidenceBrokerMatchRecord) -> Dict[str, Any]:
    return {"id": match.match_id, "outcome": match.outcome}

def compute_broker_fairness(broker: TraceEvidenceBrokerRecord) -> float:
    return 1.0

def compute_broker_pressure(broker: TraceEvidenceBrokerRecord) -> float:
    return 0.5

def preserve_fairness_without_scope_widening(broker: TraceEvidenceBrokerRecord) -> None:
    pass

def summarize_broker_pressure_and_fairness(broker: TraceEvidenceBrokerRecord) -> Dict[str, Any]:
    return {"pressure": compute_broker_pressure(broker), "fairness": compute_broker_fairness(broker)}
