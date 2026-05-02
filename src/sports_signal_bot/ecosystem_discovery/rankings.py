from typing import List
from sports_signal_bot.ecosystem_discovery.contracts import CatalogEntryRecord, ListingRankRecord

def rank_discovery_candidates(entries: List[CatalogEntryRecord]) -> List[CatalogEntryRecord]:
    # Sort by freshness, lowest is freshest
    return sorted(entries, key=lambda x: x.freshness)

def score_listing_relevance(entry: CatalogEntryRecord, query_criteria: dict) -> float:
    score = 50.0
    if entry.availability_status == "available_local":
        score += 20.0
    return score

def rank_discovery_listings(entries: List[CatalogEntryRecord]) -> List[CatalogEntryRecord]:
    return sorted(entries, key=lambda x: x.freshness)

def explain_listing_rank(rank: ListingRankRecord) -> str:
    return f"Ranked #{rank.rank} based on freshness and availability."
