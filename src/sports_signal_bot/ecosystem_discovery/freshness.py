from datetime import datetime
from sports_signal_bot.ecosystem_discovery.contracts import AssuranceRegistryCatalogRecord

def compute_catalog_freshness(last_updated: datetime) -> float:
    now = datetime.utcnow()
    delta = (now - last_updated).total_seconds() / 86400.0  # days
    return delta

def validate_catalog_supersession(catalog: AssuranceRegistryCatalogRecord) -> bool:
    # A catalog is valid if not all entries are superseded
    return any(e.availability_status != "superseded_available" for e in catalog.published_entries)

def suppress_stale_current_claims(catalog: AssuranceRegistryCatalogRecord, stale_threshold_days: float = 7.0) -> AssuranceRegistryCatalogRecord:
    for entry in catalog.published_entries:
        if entry.freshness > stale_threshold_days:
            entry.availability_status = "stale_available"
            if "Stale entry suppressed." not in entry.warnings:
                entry.warnings.append("Stale entry suppressed.")
    return catalog

def render_catalog_lifecycle_notes(catalog: AssuranceRegistryCatalogRecord) -> str:
    active = sum(1 for e in catalog.published_entries if e.availability_status == "available_local")
    superseded = sum(1 for e in catalog.published_entries if e.availability_status == "superseded_available")
    return f"Active entries: {active}, Superseded: {superseded}"
