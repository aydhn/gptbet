import pytest
from src.sports_signal_bot.proof_catalogs.atlas_federations import (
    build_evidence_atlas_federation,
    FederatedAtlasNodeRecord,
    add_atlas_federation_link,
    compute_federated_atlas_currentness
)

def test_build_federation():
    fed = build_evidence_atlas_federation("governance_evidence_atlas_federation")
    assert fed.federation_family == "governance_evidence_atlas_federation"
    assert fed.health_status == "healthy"

def test_compute_currentness():
    node1 = FederatedAtlasNodeRecord("n1", "ref1", "fam1", [], "current", "uncaveated", "safe", "active", [])
    node2 = FederatedAtlasNodeRecord("n2", "ref2", "fam2", [], "stale", "uncaveated", "safe", "active", [])
    assert compute_federated_atlas_currentness([node1, node2]) == "federated_atlas_stale"
    assert compute_federated_atlas_currentness([node1]) == "federated_atlas_current_with_caps"
