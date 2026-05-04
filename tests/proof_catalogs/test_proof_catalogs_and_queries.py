import pytest
from src.sports_signal_bot.proof_catalogs.proof_catalogs import (
    build_governance_proof_catalog,
    register_proof_catalog_entry
)

def test_build_proof_catalog():
    catalog = build_governance_proof_catalog("governance_proof_catalog")
    assert catalog.catalog_family == "governance_proof_catalog"

def test_register_entry():
    entry = register_proof_catalog_entry("replay_match_proof", "source_1", "class_1")
    assert entry.proof_family == "replay_match_proof"
    assert entry.currentness_state == "current"
