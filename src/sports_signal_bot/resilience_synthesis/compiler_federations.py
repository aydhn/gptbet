from typing import List, Optional
from datetime import datetime

from .contracts import (
    HealthCompilerFederationRecord,
    FederatedCompilerNodeRecord,
    CompilerFederationLinkRecord,
    CompilerFederationCurrentnessRecord,
    CompilerFederationHealthRecord,
    CompilerFederationScopeRecord
)

def build_health_compiler_federation(federation_id: str, family: str) -> HealthCompilerFederationRecord:
    """Builds a new health compiler federation record."""
    return HealthCompilerFederationRecord(
        compiler_federation_id=federation_id,
        federation_family=family,
        currentness_policy_ref="default_currentness_policy",
        ceiling_policy_ref="default_ceiling_policy",
        penalty_policy_ref="default_penalty_policy",
        health_status=CompilerFederationHealthRecord(
            health_id=f"h_{federation_id}",
            is_healthy=True,
            status="healthy"
        )
    )

def add_compiler_federation_link(
    federation: HealthCompilerFederationRecord,
    source_node_ref: str,
    target_node_ref: str,
    status: str = "link_current"
) -> CompilerFederationLinkRecord:
    """Adds a link between compiler nodes in the federation."""
    link_id = f"link_{source_node_ref}_{target_node_ref}"
    link = CompilerFederationLinkRecord(
        link_id=link_id,
        source_node_ref=source_node_ref,
        target_node_ref=target_node_ref,
        link_status=status
    )
    federation.federation_link_refs.append(link_id)
    return link

def validate_compiler_federation_link(link: CompilerFederationLinkRecord) -> bool:
    """Validates if a federation link is healthy and not blocked/expired."""
    return link.link_status not in ["link_blocked", "link_expired", "link_superseded"]

def compute_federated_compiler_currentness(nodes: List[FederatedCompilerNodeRecord]) -> str:
    """Computes the overall currentness of the federation based on node staleness."""
    if any(node.currentness_state.staleness_level == "expired" for node in nodes):
        return "expired"
    if any(node.currentness_state.staleness_level == "stale" for node in nodes):
        return "stale"
    return "fresh"

def summarize_compiler_federation_health(federation: HealthCompilerFederationRecord) -> dict:
    """Summarizes the health status of a compiler federation."""
    return {
        "id": federation.compiler_federation_id,
        "family": federation.federation_family,
        "links_count": len(federation.federation_link_refs),
        "status": federation.health_status.status
    }
