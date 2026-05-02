import uuid
from sports_signal_bot.ecosystem_discovery.contracts import (
    DiscoveryQuarantineRecord,
    CatalogEntryRecord
)

def quarantine_discovery_candidate(entry: CatalogEntryRecord, reason: str) -> DiscoveryQuarantineRecord:
    entry.availability_status = "quarantined"
    entry.warnings.append(reason)
    return DiscoveryQuarantineRecord(
        quarantine_id=f"quar_{uuid.uuid4().hex[:8]}",
        target_ref=entry.target_ref
    )

def release_discovery_quarantine_if_safe(entry: CatalogEntryRecord) -> bool:
    if "unsafe" not in entry.warnings:
        entry.availability_status = "available_local"
        return True
    return False

def summarize_discovery_quarantine_pressure(quarantines: list) -> dict:
    return {"total_quarantined": len(quarantines)}

def escalate_catalog_anomalies_if_needed(warnings: list) -> bool:
    return len(warnings) > 3
