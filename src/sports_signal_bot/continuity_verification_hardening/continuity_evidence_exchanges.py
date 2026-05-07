from typing import List, Dict, Any
from .contracts import (
    ContinuityEvidenceExchangeRecord,
    ContinuityEvidenceExchangeFamily,
    ContinuityEvidenceExchangeStatus,
    ContinuityEvidenceListingRecord,
    ContinuityEvidenceRequestRecord
)

def build_continuity_evidence_exchange(exchange_id: str, family: ContinuityEvidenceExchangeFamily) -> ContinuityEvidenceExchangeRecord:
    return ContinuityEvidenceExchangeRecord(
        continuity_evidence_exchange_id=exchange_id,
        exchange_family=family,
        exchange_status=ContinuityEvidenceExchangeStatus.exchange_gapped
    )

def create_continuity_evidence_listing(exchange: ContinuityEvidenceExchangeRecord, listing: ContinuityEvidenceListingRecord) -> ContinuityEvidenceExchangeRecord:
    exchange.listing_refs.append(listing.listing_id)
    return exchange

def create_continuity_evidence_request(exchange: ContinuityEvidenceExchangeRecord, request: ContinuityEvidenceRequestRecord) -> ContinuityEvidenceExchangeRecord:
    exchange.request_refs.append(request.request_id)
    return exchange

def verify_continuity_evidence_exchange(exchange: ContinuityEvidenceExchangeRecord, listings: List[ContinuityEvidenceListingRecord], has_stale: bool = False) -> ContinuityEvidenceExchangeRecord:
    if not listings:
        exchange.exchange_status = ContinuityEvidenceExchangeStatus.exchange_gapped
        return exchange

    has_caveats = len(exchange.warnings) > 0

    if has_stale:
        exchange.exchange_status = ContinuityEvidenceExchangeStatus.exchange_review_only
    elif has_caveats:
        exchange.exchange_status = ContinuityEvidenceExchangeStatus.exchange_caveated
    else:
        exchange.exchange_status = ContinuityEvidenceExchangeStatus.exchange_verified

    return exchange

def summarize_continuity_evidence_exchange(exchange: ContinuityEvidenceExchangeRecord) -> Dict[str, Any]:
    return {
        "id": exchange.continuity_evidence_exchange_id,
        "status": exchange.exchange_status,
        "listings": len(exchange.listing_refs),
        "requests": len(exchange.request_refs)
    }
