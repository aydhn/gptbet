from typing import List
from sports_signal_bot.governance_assurance.contracts import (
    ReplayMarketListingRecord,
    ListingStatus
)

def create_replay_market_listing(
    listing_id: str,
    fabric_ref: str,
    evidence_completeness: str,
    currentness_state: str
) -> ReplayMarketListingRecord:
    status = ListingStatus.LISTED_CURRENT
    warnings = []

    if evidence_completeness != "complete":
        status = ListingStatus.LISTED_CAVEATED
        warnings.append("partial_evidence_caps_listing")

    if currentness_state == "stale":
        status = ListingStatus.LISTED_REVIEW_ONLY
        warnings.append("stale_currentness_blocks_active_listing")

    return ReplayMarketListingRecord(
        listing_id=listing_id,
        listing_family="default_listing_family",
        source_fabric_ref=fabric_ref,
        replay_family="default_replay_family",
        scope_class="bounded",
        evidence_completeness=evidence_completeness,
        fidelity_band="standard",
        caveat_refs=[],
        currentness_state=currentness_state,
        listing_status=status,
        warnings=warnings
    )

def validate_replay_market_listing(listing: ReplayMarketListingRecord) -> bool:
    if listing.listing_status in [ListingStatus.LISTED_EXPIRED, ListingStatus.LISTED_SUPERSEDED, ListingStatus.LISTED_BLOCKED]:
        return False
    return True
