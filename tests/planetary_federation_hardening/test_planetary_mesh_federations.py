import pytest
from src.sports_signal_bot.planetary_federation_hardening.mesh_federations import (
    build_planetary_mesh_federation, add_mesh_federation_link, verify_planetary_mesh_federation,
    FederationFamily, FederationStatus, FederatedMeshNodeRecord, MeshFederationLinkRecord,
    MeshFederationContinuityRecord
)

def test_build_planetary_mesh_federation():
    fed = build_planetary_mesh_federation("mf-01", FederationFamily.BOUNDED_PLANETARY_MESH_FEDERATION)
    assert fed.planetary_mesh_federation_id == "mf-01"
    assert fed.federation_family == FederationFamily.BOUNDED_PLANETARY_MESH_FEDERATION

def test_verify_planetary_mesh_federation_verified():
    fed = build_planetary_mesh_federation("mf-01", FederationFamily.BOUNDED_PLANETARY_MESH_FEDERATION)
    fed.member_mesh_refs.append(FederatedMeshNodeRecord("node-01", "us-east", is_stale=False))
    add_mesh_federation_link(fed, MeshFederationLinkRecord("link-01", "node-01", "node-02", is_stale=False))
    fed.continuity_refs.append(MeshFederationContinuityRecord("cont-01", no_safe_visible=True, sovereignty_note_visible=True))

    health = verify_planetary_mesh_federation(fed)
    assert health.is_healthy
    assert health.status == FederationStatus.FEDERATION_VERIFIED

def test_verify_planetary_mesh_federation_stale():
    fed = build_planetary_mesh_federation("mf-01", FederationFamily.BOUNDED_PLANETARY_MESH_FEDERATION)
    fed.member_mesh_refs.append(FederatedMeshNodeRecord("node-01", "us-east", is_stale=True))
    add_mesh_federation_link(fed, MeshFederationLinkRecord("link-01", "node-01", "node-02", is_stale=False))
    fed.continuity_refs.append(MeshFederationContinuityRecord("cont-01", no_safe_visible=True, sovereignty_note_visible=True))

    health = verify_planetary_mesh_federation(fed)
    assert not health.is_healthy
    assert health.status == FederationStatus.FEDERATION_CAVEATED

def test_verify_planetary_mesh_federation_continuity_loss():
    fed = build_planetary_mesh_federation("mf-01", FederationFamily.BOUNDED_PLANETARY_MESH_FEDERATION)
    fed.member_mesh_refs.append(FederatedMeshNodeRecord("node-01", "us-east", is_stale=False))
    add_mesh_federation_link(fed, MeshFederationLinkRecord("link-01", "node-01", "node-02", is_stale=False))
    fed.continuity_refs.append(MeshFederationContinuityRecord("cont-01", no_safe_visible=False, sovereignty_note_visible=True))

    health = verify_planetary_mesh_federation(fed)
    assert not health.is_healthy
    assert health.status == FederationStatus.FEDERATION_BLOCKED
