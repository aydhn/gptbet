from typing import List, Dict, Any, Tuple
from sports_signal_bot.consistency_ledgers.contracts import (
    ClearingBookRecord,
    ClearingListingRecord,
    ClearingRequestRecord,
    ClearingStatus
)
from sports_signal_bot.consistency_ledgers.utils import generate_id

def build_clearing_book(
    exchange_family: str,
    scope_class: str
) -> ClearingBookRecord:
    return ClearingBookRecord(
        clearing_book_id=generate_id("clear_book"),
        exchange_family=exchange_family,
        scope_class=scope_class,
        compatible_listing_refs=[],
        compatible_request_refs=[],
        backlog_refs=[],
        pressure_state="low",
        clearing_status=ClearingStatus.CLEARING_READY,
        warnings=[]
    )

def create_clearing_listing(
    family: str,
    source_ref: str,
    source_family: str,
    trace_families: List[str],
    audience_profiles: List[str],
    completeness: float,
    caveats: List[str]
) -> ClearingListingRecord:
    return ClearingListingRecord(
        listing_id=generate_id("clear_list"),
        listing_family=family,
        source_ref=source_ref,
        source_family=source_family,
        supported_trace_families=trace_families,
        supported_audience_profiles=audience_profiles,
        evidence_completeness=completeness,
        currentness_state="current",
        caveat_refs=caveats,
        listing_status="active",
        warnings=[]
    )

def create_clearing_request(
    target_context_ref: str,
    trace_family: str,
    required_evidence: List[str],
    required_scope: str,
    required_audience: str,
    priority: str
) -> ClearingRequestRecord:
    return ClearingRequestRecord(
        request_id=generate_id("clear_req"),
        target_context_ref=target_context_ref,
        requested_trace_family=trace_family,
        required_evidence_refs=required_evidence,
        required_scope_class=required_scope,
        required_audience_profile=required_audience,
        request_priority=priority,
        request_status="pending",
        warnings=[]
    )

def ingest_clearing_listing_and_request(
    book: ClearingBookRecord,
    listing: ClearingListingRecord,
    request: ClearingRequestRecord
) -> Tuple[ClearingBookRecord, bool]:
    """Ingests into the book if compatibility baseline matches (scope doesn't widen)."""

    if listing.evidence_completeness == 0:
        listing.warnings.append("Listing has zero evidence completeness.")

    if "wide" in request.required_scope_class and "narrow" in book.scope_class:
        request.warnings.append("Scope widening blocked during ingestion.")
        book.backlog_refs.append(request.request_id)
        return book, False

    book.compatible_listing_refs.append(listing.listing_id)
    book.compatible_request_refs.append(request.request_id)
    return book, True

def validate_clearing_compatibility(
    listing: ClearingListingRecord,
    request: ClearingRequestRecord
) -> Tuple[bool, List[str]]:
    """Validates if a listing can satisfy a request."""
    warnings = []

    if request.requested_trace_family not in listing.supported_trace_families:
        warnings.append(f"Trace family mismatch: {request.requested_trace_family} not in {listing.supported_trace_families}")

    if request.required_audience_profile not in listing.supported_audience_profiles:
        warnings.append(f"Audience profile mismatch: {request.required_audience_profile} not in {listing.supported_audience_profiles}")

    if listing.currentness_state != "current":
        warnings.append("Listing is stale.")

    is_compatible = len(warnings) == 0 or (len(warnings) == 1 and listing.currentness_state != "current") # Still compatible but degraded

    return is_compatible, warnings

def explain_clearing_mismatch(listing: ClearingListingRecord, request: ClearingRequestRecord, warnings: List[str]) -> Dict[str, Any]:
    return {
        "listing_id": listing.listing_id,
        "request_id": request.request_id,
        "mismatch_reasons": warnings
    }
