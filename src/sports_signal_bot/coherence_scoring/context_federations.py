import uuid
from typing import List, Dict, Any
from .contracts import (
    ContextAssemblerFederationRecord,
    FederatedContextNodeRecord,
    ContextFederationLinkRecord,
    ContextFederationBundleRecord
)

# FEDERATION LINK STATUS TAXONOMY
LINK_CURRENT = "link_current"
LINK_CAVEATED = "link_caveated"
LINK_REVIEW_ONLY = "link_review_only"
LINK_DEGRADED = "link_degraded"
LINK_BLOCKED = "link_blocked"
LINK_EXPIRED = "link_expired"
LINK_SUPERSEDED = "link_superseded"

# CONTEXT FEDERATION FAMILY TAXONOMY
OPERATOR_CONTEXT_FEDERATION = "operator_context_federation"
REVIEWER_CONTEXT_FEDERATION = "reviewer_context_federation"
EXECUTIVE_CONTEXT_FEDERATION = "executive_context_federation"
SOVEREIGNTY_PRESERVATION_CONTEXT_FEDERATION = "sovereignty_preservation_context_federation"
REPLAY_AND_DEBT_CONTEXT_FEDERATION = "replay_and_debt_context_federation"
NO_SAFE_VISIBILITY_CONTEXT_FEDERATION = "no_safe_visibility_context_federation"
COMPOSITE_GOVERNANCE_CONTEXT_FEDERATION = "composite_governance_context_federation"

# FEDERATED CONTEXT OUTPUT TAXONOMY
FEDERATED_CONTEXT_CURRENT_WITH_CAPS = "federated_context_current_with_caps"
FEDERATED_CONTEXT_CAVEATED = "federated_context_caveated"
FEDERATED_CONTEXT_REVIEW_ONLY = "federated_context_review_only"
FEDERATED_CONTEXT_DEGRADED = "federated_context_degraded"
FEDERATED_CONTEXT_BLOCKED = "federated_context_blocked"
FEDERATED_CONTEXT_STALE = "federated_context_stale"

def build_context_assembler_federation(family: str, policy_refs: Dict[str, str]) -> ContextAssemblerFederationRecord:
    return ContextAssemblerFederationRecord(
        context_federation_id=str(uuid.uuid4()),
        federation_family=family,
        currentness_policy_ref=policy_refs.get('currentness', 'default'),
        audience_policy_ref=policy_refs.get('audience', 'default'),
        scope_policy_ref=policy_refs.get('scope', 'default'),
        health_status="initializing"
    )

def add_context_federation_link(federation: ContextAssemblerFederationRecord, node: FederatedContextNodeRecord) -> ContextFederationLinkRecord:
    link_id = str(uuid.uuid4())
    federation.member_context_assembler_refs.append(node.node_id)
    federation.active_link_refs.append(link_id)
    return ContextFederationLinkRecord(link_id=link_id, status=LINK_CURRENT)

def validate_context_federation_link(link: ContextFederationLinkRecord, node: FederatedContextNodeRecord) -> None:
    if node.currentness_state == "stale":
        link.status = LINK_DEGRADED

def compute_federated_context_currentness(federation: ContextAssemblerFederationRecord, nodes: List[FederatedContextNodeRecord]) -> str:
    if any(node.currentness_state == "stale" for node in nodes):
        return FEDERATED_CONTEXT_STALE
    elif any(node.currentness_state == "caveated" for node in nodes):
        return FEDERATED_CONTEXT_CAVEATED
    return FEDERATED_CONTEXT_CURRENT_WITH_CAPS

def summarize_context_federation_health(federation: ContextAssemblerFederationRecord) -> Dict[str, Any]:
    return {
        "id": federation.context_federation_id,
        "members": len(federation.member_context_assembler_refs),
        "links": len(federation.active_link_refs),
        "status": federation.health_status,
        "warnings": federation.warnings
    }

def aggregate_federated_context_bundles(federation: ContextAssemblerFederationRecord, bundles: List[Dict]) -> ContextFederationBundleRecord:
    record = ContextFederationBundleRecord(
        bundle_id=str(uuid.uuid4()),
        no_safe_visibility_state="preserved",
        output_scope="bounded"
    )
    for b in bundles:
        record.source_context_refs.append(b.get('id', ''))
    return record

def preserve_caveats_and_sections_in_context_federation(bundle: ContextFederationBundleRecord, caveats: List[str]) -> None:
    bundle.preserved_caveat_refs.extend(caveats)

def preserve_no_safe_context_in_federation(bundle: ContextFederationBundleRecord) -> None:
    bundle.no_safe_visibility_state = "preserved"

def explain_federated_context_output(bundle: ContextFederationBundleRecord) -> str:
    return f"Federated bundle {bundle.bundle_id} with scope {bundle.output_scope} and caveats {bundle.preserved_caveat_refs}"
