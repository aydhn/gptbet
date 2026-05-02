from datetime import datetime
import uuid
from sports_signal_bot.ecosystem_discovery.contracts import (
    AssuranceRegistryCatalogRecord,
    CatalogEntryRecord
)

def build_assurance_registry_catalog(catalog_name: str, owner_registry_ref: str, catalog_family: str = "registry_catalog") -> AssuranceRegistryCatalogRecord:
    return AssuranceRegistryCatalogRecord(
        catalog_id=f"cat_{uuid.uuid4().hex[:8]}",
        catalog_name=catalog_name,
        catalog_family=catalog_family,
        owner_registry_ref=owner_registry_ref,
        trust_profile="unverified",
        freshness_state="current",
        active_status="active"
    )

def add_catalog_entry(catalog: AssuranceRegistryCatalogRecord, entry: CatalogEntryRecord) -> AssuranceRegistryCatalogRecord:
    catalog.published_entries.append(entry)
    return catalog

def validate_catalog_entry(entry: CatalogEntryRecord) -> bool:
    if not entry.entry_id or not entry.target_ref:
        return False
    return True

def summarize_catalog_state(catalog: AssuranceRegistryCatalogRecord) -> dict:
    return {
        "catalog_id": catalog.catalog_id,
        "entry_count": len(catalog.published_entries),
        "trust_profile": catalog.trust_profile,
        "freshness": catalog.freshness_state
    }

def mark_catalog_entry_superseded(catalog: AssuranceRegistryCatalogRecord, entry_id: str) -> AssuranceRegistryCatalogRecord:
    for entry in catalog.published_entries:
        if entry.entry_id == entry_id:
            entry.availability_status = "superseded_available"
            entry.warnings.append("Superseded by a newer entry.")
    return catalog
