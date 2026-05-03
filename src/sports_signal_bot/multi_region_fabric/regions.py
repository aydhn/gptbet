from typing import List, Optional
from sports_signal_bot.multi_region_fabric.contracts import RegionRecord

# Taxonomy constants
REGION_FAMILIES = [
    "primary_execution_region",
    "secondary_execution_region",
    "review_only_region",
    "rollback_reserve_region",
    "closure_priority_region",
    "federated_partner_region",
    "sovereignty_restricted_region"
]

def build_region(region_id: str, family: str, desc: str) -> RegionRecord:
    if family not in REGION_FAMILIES:
        raise ValueError(f"Unknown region family: {family}")
    return RegionRecord(region_id=region_id, region_family=family, description=desc)
