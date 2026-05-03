from sports_signal_bot.multi_region_fabric.contracts import RegionalListingVisibilityRecord

def derive_region_specific_listing_visibility(list_id: str, region: str) -> RegionalListingVisibilityRecord:
    return RegionalListingVisibilityRecord(listing_id=list_id, region_id=region, visibility="visible")

def validate_listing_against_sovereignty(list_id: str, policy_id: str) -> bool:
    return True

def summarize_listing_region_fit(list_id: str) -> str:
    return f"Listing {list_id} fits."
