from typing import List, Dict, Optional
from sports_signal_bot.corridor_governance.contracts import (
    CorridorCatalogRecord,
    CorridorCatalogEntryRecord,
    CorridorDiscoverabilityRecord
)

def build_corridor_catalog(entries: List[CorridorCatalogEntryRecord]) -> CorridorCatalogRecord:
    return CorridorCatalogRecord(entries=entries)

def add_corridor_catalog_entry(
    catalog: CorridorCatalogRecord, entry: CorridorCatalogEntryRecord
) -> CorridorCatalogRecord:
    catalog.entries.append(entry)
    return catalog

def validate_corridor_catalog_entry(entry: CorridorCatalogEntryRecord) -> bool:
    if not entry.corridor_ref or not entry.treaty_ref:
        return False
    return True

def compute_corridor_discoverability(entry: CorridorCatalogEntryRecord) -> CorridorDiscoverabilityRecord:
    # A simplified stub for discoverability logic
    status = "discoverable_internal"
    if entry.supersession_state == "superseded":
        status = "hidden_by_supersession"
    elif entry.freshness_state == "stale":
        status = "hidden_by_expiry"

    return CorridorDiscoverabilityRecord(
        corridor_ref=entry.corridor_ref,
        discoverability_status=status
    )

def summarize_corridor_catalog_health(catalog: CorridorCatalogRecord) -> Dict[str, int]:
    summary = {
        "total_entries": len(catalog.entries),
        "active_entries": 0,
        "superseded_entries": 0,
        "stale_entries": 0
    }
    for entry in catalog.entries:
        if entry.supersession_state == "superseded":
            summary["superseded_entries"] += 1
        elif entry.freshness_state == "stale":
            summary["stale_entries"] += 1
        else:
            summary["active_entries"] += 1
    return summary
