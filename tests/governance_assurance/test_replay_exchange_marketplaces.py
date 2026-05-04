import pytest
from sports_signal_bot.governance_assurance.contracts import (
    ReplayMarketplaceFamily, ListingStatus
)
from sports_signal_bot.governance_assurance.replay_marketplaces import (
    build_replay_exchange_marketplace, summarize_replay_marketplace
)
from sports_signal_bot.governance_assurance.listings import (
    create_replay_market_listing, validate_replay_market_listing
)

def test_build_replay_exchange_marketplace():
    marketplace = build_replay_exchange_marketplace("m1", ReplayMarketplaceFamily.BOUNDED_REPLAY)
    assert marketplace.replay_marketplace_id == "m1"

    summary = summarize_replay_marketplace(marketplace)
    assert summary["health"] == "healthy"

def test_create_and_validate_replay_market_listing():
    listing = create_replay_market_listing("l1", "fab1", "partial", "current")
    assert listing.listing_status == ListingStatus.LISTED_CAVEATED
    assert validate_replay_market_listing(listing) == True

    listing_stale = create_replay_market_listing("l2", "fab2", "complete", "stale")
    assert listing_stale.listing_status == ListingStatus.LISTED_REVIEW_ONLY
