import pytest
from src.sports_signal_bot.trace_routing.contracts import (
    ProofFederationFamily,
    FederatedProofNodeRecord,
    FederationLinkStatus,
    FederatedProofOutput
)
from src.sports_signal_bot.trace_routing.proof_federations import (
    build_proof_catalog_federation,
    add_proof_federation_link,
    validate_proof_federation_link,
    compute_federated_proof_currentness,
    aggregate_federated_proofs
)

def test_build_proof_catalog_federation():
    fed = build_proof_catalog_federation(
        ProofFederationFamily.GOVERNANCE_PROOF_CATALOG_FEDERATION,
        "policy_ref", "lineage_ref", "app_ref"
    )
    assert fed.federation_family == ProofFederationFamily.GOVERNANCE_PROOF_CATALOG_FEDERATION
    assert fed.health_status == "healthy"

def test_proof_federation_aggregation_stale():
    fed = build_proof_catalog_federation(
        ProofFederationFamily.GOVERNANCE_PROOF_CATALOG_FEDERATION,
        "policy_ref", "lineage_ref", "app_ref"
    )
    nodes = [
        FederatedProofNodeRecord(
            node_id="n1", proof_catalog_ref="pc1", proof_catalog_family="fam",
            currentness_state="stale", caveat_state="clean", sovereignty_state="clean", node_status="active"
        )
    ]
    output = aggregate_federated_proofs(fed, nodes)
    assert output == FederatedProofOutput.FEDERATED_PROOF_STALE

def test_proof_federation_aggregation_sovereignty_warning():
    fed = build_proof_catalog_federation(
        ProofFederationFamily.GOVERNANCE_PROOF_CATALOG_FEDERATION,
        "policy_ref", "lineage_ref", "app_ref"
    )
    nodes = [
        FederatedProofNodeRecord(
            node_id="n1", proof_catalog_ref="pc1", proof_catalog_family="fam",
            currentness_state="current", caveat_state="clean", sovereignty_state="warning", node_status="active"
        )
    ]
    output = aggregate_federated_proofs(fed, nodes)
    assert output == FederatedProofOutput.FEDERATED_PROOF_REVIEW_ONLY
