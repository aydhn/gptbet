from typing import List
from sports_signal_bot.federation_ecosystem.contracts import (
    TreatyBaselineCatalogRecord, BaselineCatalogEntryRecord
)

def build_baseline_catalog(catalog_id: str, family: str) -> TreatyBaselineCatalogRecord:
    return TreatyBaselineCatalogRecord(
        catalog_id=catalog_id,
        entries=[],
        catalog_family=family,
        health_status="healthy",
        warnings=[]
    )

def register_baseline_catalog_entry(catalog: TreatyBaselineCatalogRecord, entry: BaselineCatalogEntryRecord) -> TreatyBaselineCatalogRecord:
    catalog.entries.append(entry)
    return catalog

def validate_baseline_catalog_entry(entry: BaselineCatalogEntryRecord) -> bool:
    return entry.discoverability_state not in ["hidden_superseded", "hidden_expired"]

def summarize_baseline_catalog_health(catalog: TreatyBaselineCatalogRecord) -> str:
    return catalog.health_status

def project_catalog_currentness(entry: BaselineCatalogEntryRecord) -> str:
    if entry.freshness_state == "stale":
        return "stale_projection"
    return "current_projection"
