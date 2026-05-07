from typing import List
from .contracts import (
    PlanetaryMeshFederationRecord, FederationFamily, FederationStatus,
    FederatedMeshNodeRecord, MeshFederationLinkRecord, MeshFederationAgreementRecord,
    MeshFederationLagRecord, MeshFederationCaveatRecord, MeshFederationContinuityRecord,
    MeshFederationResidueRecord, PlanetaryMeshFederationHealthRecord,
    PlanetaryMeshFederationWarningRecord
)

def build_planetary_mesh_federation(federation_id: str, family: FederationFamily) -> PlanetaryMeshFederationRecord:
    return PlanetaryMeshFederationRecord(
        planetary_mesh_federation_id=federation_id,
        federation_family=family
    )

def add_mesh_federation_link(federation: PlanetaryMeshFederationRecord, link: MeshFederationLinkRecord) -> None:
    federation.active_link_refs.append(link)

def verify_planetary_mesh_federation(federation: PlanetaryMeshFederationRecord) -> PlanetaryMeshFederationHealthRecord:
    stale_nodes = [n for n in federation.member_mesh_refs if n.is_stale]
    stale_links = [l for l in federation.active_link_refs if l.is_stale]
    missing_continuity = [c for c in federation.continuity_refs if not c.no_safe_visible or not c.sovereignty_note_visible]

    if stale_nodes or stale_links:
        federation.federation_status = FederationStatus.FEDERATION_CAVEATED
        federation.warnings.append(PlanetaryMeshFederationWarningRecord(
            warning_id="stale_members",
            severity="high",
            description="Federation contains stale members or links, capping agreement quality."
        ))
        return PlanetaryMeshFederationHealthRecord(is_healthy=False, status=FederationStatus.FEDERATION_CAVEATED, details="Stale members found.")

    if missing_continuity:
        federation.federation_status = FederationStatus.FEDERATION_BLOCKED
        federation.warnings.append(PlanetaryMeshFederationWarningRecord(
            warning_id="missing_continuity",
            severity="critical",
            description="No-safe or sovereignty continuity lost across federation boundary."
        ))
        return PlanetaryMeshFederationHealthRecord(is_healthy=False, status=FederationStatus.FEDERATION_BLOCKED, details="Continuity loss.")

    if not federation.active_link_refs:
        federation.federation_status = FederationStatus.FEDERATION_GAPPED
        return PlanetaryMeshFederationHealthRecord(is_healthy=False, status=FederationStatus.FEDERATION_GAPPED, details="No links found.")

    federation.federation_status = FederationStatus.FEDERATION_VERIFIED
    return PlanetaryMeshFederationHealthRecord(is_healthy=True, status=FederationStatus.FEDERATION_VERIFIED, details="Federation verified.")

def compute_mesh_federation_agreement(federation: PlanetaryMeshFederationRecord) -> MeshFederationAgreementRecord:
    # A simple mock agreement computation
    if federation.federation_status == FederationStatus.FEDERATION_VERIFIED:
        return MeshFederationAgreementRecord(agreement_id="ag-01", band="stable_agreement")
    return MeshFederationAgreementRecord(agreement_id="ag-02", band="weak_agreement")

def summarize_planetary_mesh_federation(federation: PlanetaryMeshFederationRecord) -> dict:
    return {
        "id": federation.planetary_mesh_federation_id,
        "family": federation.federation_family.value,
        "status": federation.federation_status.value,
        "warnings_count": len(federation.warnings)
    }
