from sports_signal_bot.ecosystem_discovery.quarantine import (
    quarantine_discovery_candidate,
    release_discovery_quarantine_if_safe
)
from sports_signal_bot.ecosystem_discovery.contracts import CatalogEntryRecord

def test_quarantine():
    entry = CatalogEntryRecord(
        entry_id="ent_1",
        entry_family="test",
        target_ref="trg",
        display_name="test",
        availability_status="available_local",
        freshness=0.0
    )

    q_rec = quarantine_discovery_candidate(entry, "unsafe")
    assert entry.availability_status == "quarantined"
    assert "unsafe" in entry.warnings

    res = release_discovery_quarantine_if_safe(entry)
    assert not res
    assert entry.availability_status == "quarantined"
