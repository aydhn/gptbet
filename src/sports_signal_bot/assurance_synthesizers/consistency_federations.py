from typing import List, Optional, Dict
import uuid
from datetime import datetime

from src.sports_signal_bot.assurance_synthesizers.contracts import (
    ConsistencyLedgerFederationRecord,
    FederatedConsistencyNodeRecord,
    ConsistencyFederationLinkRecord,
    LinkStatus
)

def build_consistency_ledger_federation(
    federation_family: str,
    currentness_policy_ref: str,
    contradiction_policy_ref: str,
    ceiling_policy_ref: str
) -> ConsistencyLedgerFederationRecord:
    """Builds a bounded consistency federation."""
    return ConsistencyLedgerFederationRecord(
        consistency_federation_id=f"fed_{uuid.uuid4().hex[:8]}",
        federation_family=federation_family,
        currentness_policy_ref=currentness_policy_ref,
        contradiction_policy_ref=contradiction_policy_ref,
        ceiling_policy_ref=ceiling_policy_ref,
        health_status="initializing"
    )

def add_consistency_federation_link(
    federation: ConsistencyLedgerFederationRecord,
    source_node: FederatedConsistencyNodeRecord,
    target_node: FederatedConsistencyNodeRecord
) -> ConsistencyFederationLinkRecord:
    """Adds a link between nodes, preserving contradictions."""
    link = ConsistencyFederationLinkRecord(
        link_id=f"link_{uuid.uuid4().hex[:8]}",
        source_node_ref=source_node.node_id,
        target_node_ref=target_node.node_id,
        link_status=LinkStatus.link_current
    )
    if "stale" in source_node.currentness_state or "stale" in target_node.currentness_state:
        link.link_status = LinkStatus.link_caveated
        federation.warnings.append(f"Stale node detected in link {link.link_id}")

    if "no_safe" in source_node.sovereignty_state or "deny" in source_node.sovereignty_state:
        link.link_status = LinkStatus.link_degraded
        federation.warnings.append(f"Sovereignty limits or no_safe context present in link {link.link_id}")

    federation.active_link_refs.append(link.link_id)
    return link

def compute_federated_consistency_currentness(
    federation: ConsistencyLedgerFederationRecord,
    nodes: List[FederatedConsistencyNodeRecord]
) -> str:
    """Computes overall currentness. Cap if any node is stale."""
    for node in nodes:
        if "stale" in node.currentness_state:
            return "stale_currentness_capped"
    return "current"

def summarize_consistency_federation_health(federation: ConsistencyLedgerFederationRecord) -> Dict[str, str]:
    return {
        "id": federation.consistency_federation_id,
        "family": federation.federation_family,
        "health": federation.health_status,
        "warning_count": str(len(federation.warnings))
    }
