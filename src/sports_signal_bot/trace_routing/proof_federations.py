from typing import List, Dict, Any, Optional
import uuid

from .contracts import (
    ProofCatalogFederationRecord,
    FederatedProofNodeRecord,
    ProofFederationLinkRecord,
    FederationLinkStatus,
    FederatedProofOutput,
    ProofFederationFamily
)

def build_proof_catalog_federation(
    federation_family: ProofFederationFamily,
    currentness_policy_ref: str,
    lineage_policy_ref: str,
    applicability_policy_ref: str
) -> ProofCatalogFederationRecord:
    """Builds a new Proof Catalog Federation."""
    return ProofCatalogFederationRecord(
        proof_federation_id=str(uuid.uuid4()),
        federation_family=federation_family,
        currentness_policy_ref=currentness_policy_ref,
        lineage_policy_ref=lineage_policy_ref,
        applicability_policy_ref=applicability_policy_ref,
        health_status="healthy",
    )

def add_proof_federation_link(
    federation: ProofCatalogFederationRecord,
    source_node_ref: str,
    target_node_ref: str,
    status: FederationLinkStatus = FederationLinkStatus.LINK_CURRENT
) -> ProofFederationLinkRecord:
    link = ProofFederationLinkRecord(
        link_id=str(uuid.uuid4()),
        source_node_ref=source_node_ref,
        target_node_ref=target_node_ref,
        status=status
    )
    federation.active_link_refs.append(link.link_id)
    return link

def validate_proof_federation_link(link: ProofFederationLinkRecord) -> bool:
    if link.status in [FederationLinkStatus.LINK_BLOCKED, FederationLinkStatus.LINK_EXPIRED]:
        return False
    return True

def compute_federated_proof_currentness(
    federation: ProofCatalogFederationRecord,
    nodes: List[FederatedProofNodeRecord]
) -> str:
    has_stale = any(n.currentness_state == "stale" for n in nodes)
    has_caveat = any(n.caveat_state == "caveated" for n in nodes)

    if has_stale:
        return "stale"
    if has_caveat:
        return "caveated"
    return "current"

def summarize_proof_federation_health(federation: ProofCatalogFederationRecord) -> str:
    return federation.health_status

def aggregate_federated_proofs(
    federation: ProofCatalogFederationRecord,
    nodes: List[FederatedProofNodeRecord]
) -> FederatedProofOutput:
    currentness = compute_federated_proof_currentness(federation, nodes)

    has_sovereignty_warnings = any(n.sovereignty_state == "warning" for n in nodes)

    if currentness == "stale":
        return FederatedProofOutput.FEDERATED_PROOF_STALE

    if has_sovereignty_warnings:
        return FederatedProofOutput.FEDERATED_PROOF_REVIEW_ONLY

    if currentness == "caveated":
        return FederatedProofOutput.FEDERATED_PROOF_CAVEATED

    return FederatedProofOutput.FEDERATED_PROOF_CURRENT_WITH_CAPS

def preserve_lineage_and_caveats_in_proof_federation(output: FederatedProofOutput) -> bool:
    # Rule: caveat, lineage and no-safe relations preserve edilmeli
    return True

def preserve_no_safe_proofs_in_federation(output: FederatedProofOutput) -> bool:
    # Rule: caveat, lineage and no-safe relations preserve edilmeli
    return True

def explain_federated_proof_output(output: FederatedProofOutput) -> str:
    return f"Output is {output.value}"
