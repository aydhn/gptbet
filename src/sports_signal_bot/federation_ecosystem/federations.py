from typing import List, Dict, Optional
from sports_signal_bot.federation_ecosystem.contracts import (
    CorridorRegistryFederationRecord, FederationLinkRecord, FederatedRegistryNodeRecord
)

def build_registry_federation(federation_id: str, family: str, registries: List[str]) -> CorridorRegistryFederationRecord:
    return CorridorRegistryFederationRecord(
        federation_id=federation_id,
        federation_family=family,
        member_registry_refs=registries,
        active_link_refs=[],
        supported_entry_families=[],
        currentness_policy_ref="default",
        visibility_policy_ref="default",
        health_status="healthy",
        warnings=[]
    )

def add_federation_link(federation: CorridorRegistryFederationRecord, link: FederationLinkRecord) -> CorridorRegistryFederationRecord:
    federation.active_link_refs.append(link.link_id)
    return federation

def validate_federation_link(link: FederationLinkRecord) -> bool:
    return link.link_status not in ["linked_degraded", "linked_expired", "linked_suspended", "linked_superseded"]

def compute_federated_currentness(source_currentness: str, link_status: str) -> str:
    if link_status in ["linked_degraded", "linked_expired", "linked_suspended", "linked_superseded"]:
        return "stale"
    return "current_with_caveats" if link_status == "linked_caveated" else "current"

def summarize_federation_health(federation: CorridorRegistryFederationRecord) -> str:
    return federation.health_status
