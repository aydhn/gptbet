import pytest
from sports_signal_bot.corridor_governance.contracts import CorridorCatalogEntryRecord
from sports_signal_bot.corridor_governance.catalogs import (
    build_corridor_catalog,
    add_corridor_catalog_entry,
    validate_corridor_catalog_entry,
    compute_corridor_discoverability
)

def test_corridor_catalog_building():
    entry = CorridorCatalogEntryRecord(
        catalog_entry_id="cat-1", corridor_ref="corr-1", source_region_ref="r1", target_region_ref="r2",
        treaty_ref="t1", allowed_lane_families=["review"], allowed_transfer_classes=["min"],
        continuity_requirement_summary="req", translation_requirement_summary="req",
        sovereignty_notes="ok", freshness_state="current", supersession_state="active",
        visibility_profile="internal", warnings=[]
    )
    catalog = build_corridor_catalog([entry])
    assert len(catalog.entries) == 1
    assert catalog.entries[0].catalog_entry_id == "cat-1"

def test_validate_catalog_entry():
    valid_entry = CorridorCatalogEntryRecord(
        catalog_entry_id="cat-1", corridor_ref="corr-1", source_region_ref="r1", target_region_ref="r2",
        treaty_ref="t1", allowed_lane_families=[], allowed_transfer_classes=[],
        continuity_requirement_summary="", translation_requirement_summary="",
        sovereignty_notes="", freshness_state="", supersession_state="",
        visibility_profile="", warnings=[]
    )
    assert validate_corridor_catalog_entry(valid_entry) == True

def test_compute_discoverability_superseded():
    entry = CorridorCatalogEntryRecord(
        catalog_entry_id="cat-1", corridor_ref="corr-1", source_region_ref="r1", target_region_ref="r2",
        treaty_ref="t1", allowed_lane_families=[], allowed_transfer_classes=[],
        continuity_requirement_summary="", translation_requirement_summary="",
        sovereignty_notes="", freshness_state="", supersession_state="superseded",
        visibility_profile="", warnings=[]
    )
    disc = compute_corridor_discoverability(entry)
    assert disc.discoverability_status == "hidden_by_supersession"
