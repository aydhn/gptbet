from typing import List, Dict, Any
from sports_signal_bot.governance_assurance.contracts import (
    ReplayExchangeMarketplaceRecord,
    ReplayMarketplaceFamily,
    ReplayExchangeMarketplaceWarningRecord
)

def build_replay_exchange_marketplace(
    marketplace_id: str,
    family: ReplayMarketplaceFamily
) -> ReplayExchangeMarketplaceRecord:
    return ReplayExchangeMarketplaceRecord(
        replay_marketplace_id=marketplace_id,
        marketplace_family=family,
        active_listing_refs=[],
        active_offer_refs=[],
        active_request_refs=[],
        active_match_refs=[],
        matching_policy_ref="bounded_matching_policy",
        fairness_policy_ref="default_fairness_policy",
        health_status="healthy",
        warnings=[]
    )

def summarize_replay_marketplace(marketplace: ReplayExchangeMarketplaceRecord) -> Dict[str, Any]:
    return {
        "marketplace_id": marketplace.replay_marketplace_id,
        "family": marketplace.marketplace_family.value,
        "active_listings": len(marketplace.active_listing_refs),
        "active_offers": len(marketplace.active_offer_refs),
        "active_requests": len(marketplace.active_request_refs),
        "active_matches": len(marketplace.active_match_refs),
        "health": marketplace.health_status
    }
