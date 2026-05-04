import uuid
from typing import List
from .contracts import (
    EvidenceAtlasFederationRecord,
    FederatedAtlasNodeRecord,
    AtlasFederationLinkRecord
)

def build_evidence_atlas_federation(federation_family: str) -> EvidenceAtlasFederationRecord:
    return EvidenceAtlasFederationRecord(
        atlas_federation_id=str(uuid.uuid4()),
        federation_family=federation_family,
        member_atlas_refs=[],
        active_link_refs=[],
        currentness_policy_ref="default_currentness_policy",
        lineage_policy_ref="default_lineage_policy",
        applicability_policy_ref="default_applicability_policy",
        health_status="healthy",
        warnings=[]
    )

def add_atlas_federation_link(source_node: FederatedAtlasNodeRecord, target_node: FederatedAtlasNodeRecord) -> AtlasFederationLinkRecord:
    return AtlasFederationLinkRecord(
        link_id=str(uuid.uuid4()),
        source_node_ref=source_node.node_id,
        target_node_ref=target_node.node_id,
        link_status="link_current",
        warnings=[]
    )

def validate_atlas_federation_link(link: AtlasFederationLinkRecord) -> bool:
    if not link.source_node_ref or not link.target_node_ref:
        return False
    return True

def compute_federated_atlas_currentness(nodes: List[FederatedAtlasNodeRecord]) -> str:
    if not nodes:
        return "stale"
    for node in nodes:
        if node.currentness_state == "stale":
            return "federated_atlas_stale"
    return "federated_atlas_current_with_caps"

def summarize_atlas_federation_health(federation: EvidenceAtlasFederationRecord) -> str:
    if federation.warnings:
        return "degraded"
    return federation.health_status

def aggregate_federated_atlas_views(federation: EvidenceAtlasFederationRecord) -> str:
    return "aggregated_view"

def preserve_lineage_and_caveats_in_federation(federation: EvidenceAtlasFederationRecord) -> None:
    pass

def preserve_no_safe_edges_in_federation(federation: EvidenceAtlasFederationRecord) -> None:
    pass

def explain_federated_atlas_output(federation: EvidenceAtlasFederationRecord) -> str:
    return f"Federated atlas {federation.atlas_federation_id} with family {federation.federation_family}"
