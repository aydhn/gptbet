from typing import List
from sports_signal_bot.multi_region_fabric.contracts import CrossRegionContentionRecord

CONTENTION_FAMILIES = [
    "same source surface claimed across regions",
    "rollback reserve conflict across clusters",
    "closure observer overload across regions",
    "replay budget contention across sovereignty domains",
    "federated listing mismatch across regions",
    "shard ownership collision across broker shards",
    "cross-region approval freshness mismatch",
    "treaty interpretation mismatch"
]

OUTCOMES = [
    "region_serialize",
    "keep_local_dominant",
    "reserve_for_source_region",
    "external_assist_review_only",
    "deny_cross_region_parallelism",
    "council_escalation_required",
    "treaty_clarification_required"
]

def detect_cross_region_contentions(regions: List[str]) -> List[CrossRegionContentionRecord]:
    if len(regions) > 1:
        return [CrossRegionContentionRecord(
            contention_id="c_1",
            contention_family="same source surface claimed across regions",
            regions_involved=regions,
            outcome="region_serialize"
        )]
    return []

def classify_region_contention(c: CrossRegionContentionRecord) -> str:
    return c.contention_family

def escalate_to_council_or_treaty_review(c: CrossRegionContentionRecord) -> bool:
    return True

def summarize_cross_region_pressure(cs: List[CrossRegionContentionRecord]) -> str:
    return f"{len(cs)} contentions detected."
