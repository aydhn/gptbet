from sports_signal_bot.ecosystem_discovery.catalogs import (
    build_assurance_registry_catalog,
    add_catalog_entry,
    validate_catalog_entry,
    mark_catalog_entry_superseded
)
from sports_signal_bot.ecosystem_discovery.contracts import CatalogEntryRecord

def test_build_and_add_catalog():
    cat = build_assurance_registry_catalog("test_cat", "reg_123")
    assert cat.catalog_name == "test_cat"

    entry = CatalogEntryRecord(
        entry_id="ent_1",
        entry_family="registry_capability_entry",
        target_ref="trg_1",
        display_name="Test Entry",
        availability_status="available_local",
        freshness=0.0
    )
    assert validate_catalog_entry(entry)

    cat = add_catalog_entry(cat, entry)
    assert len(cat.published_entries) == 1

    cat = mark_catalog_entry_superseded(cat, "ent_1")
    assert cat.published_entries[0].availability_status == "superseded_available"
