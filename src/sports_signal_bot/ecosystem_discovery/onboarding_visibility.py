from sports_signal_bot.ecosystem_discovery.contracts import CatalogEntryRecord

def publish_onboarded_verifier_to_catalog(verifier_id: str) -> CatalogEntryRecord:
    import uuid
    return CatalogEntryRecord(
        entry_id=f"ver_{uuid.uuid4().hex[:8]}",
        entry_family="verifier_capability_entry",
        target_ref=verifier_id,
        display_name=f"Verifier {verifier_id}",
        availability_status="available_local",
        freshness=0.0
    )

def hide_or_downgrade_problematic_verifier_listing(entry: CatalogEntryRecord) -> CatalogEntryRecord:
    entry.availability_status = "quarantined"
    return entry

def refresh_listing_after_onboarding_change(entry: CatalogEntryRecord) -> CatalogEntryRecord:
    entry.freshness = 0.0
    return entry

def summarize_onboarding_visibility(entry: CatalogEntryRecord) -> dict:
    return {
        "entry_id": entry.entry_id,
        "status": entry.availability_status
    }
