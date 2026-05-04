from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any, Literal

class FederationLinkRecord(BaseModel):
    link_id: str
    source_registry_ref: str
    target_registry_ref: str
    link_status: Literal[
        "linked_review_only", "linked_bounded_exchange", "linked_catalog_visibility",
        "linked_caveated", "linked_degraded", "linked_expired", "linked_suspended", "linked_superseded"
    ]
    caveats: List[str] = Field(default_factory=list)

class CorridorRegistryFederationRecord(BaseModel):
    federation_id: str
    federation_family: Literal[
        "sovereign_corridor_registry_federation", "treaty_registry_federation",
        "continuity_attestation_registry_federation", "baseline_catalog_federation",
        "conformance_pack_federation", "review_only_registry_federation", "internal_preview_registry_federation"
    ]
    member_registry_refs: List[str]
    active_link_refs: List[str]
    supported_entry_families: List[str]
    currentness_policy_ref: str
    visibility_policy_ref: str
    health_status: Literal["healthy", "caution", "federation_stale", "exchange_stressed", "pack_gap_heavy", "degraded", "blocked"]
    warnings: List[str] = Field(default_factory=list)

class FederatedRegistryNodeRecord(BaseModel):
    node_id: str
    registry_ref: str
    node_family: str
    supported_entry_families: List[str]
    supported_exchange_families: List[str]
    currentness_state: str
    freshness_state: str
    visibility_profile: str
    warnings: List[str] = Field(default_factory=list)

class FederatedCurrentPointerRecord(BaseModel):
    source_currentness: str
    federated_currentness_projection: str
    successor_link: Optional[str]
    source_freshness: str
    federation_freshness: str
    replay_requirement: str
    local_trust_caveat: Optional[str]

class AttestationExchangeHubRecord(BaseModel):
    hub_id: str
    hub_family: Literal[
        "internal_attestation_hub", "treaty_bound_attestation_hub", "review_only_attestation_hub",
        "benchmark_support_hub", "continuity_summary_hub", "policy_conformance_hub", "degraded_exchange_hub"
    ]
    supported_attestation_families: List[str]
    supported_exchange_scopes: List[str]
    participant_refs: List[str]
    queue_refs: List[str]
    routing_policy_ref: str
    health_status: str
    warnings: List[str] = Field(default_factory=list)

class HubAdmissionRecord(BaseModel):
    admission_id: str
    incoming_packet_ref: str
    source_registry_ref: str
    target_registry_refs: List[str]
    requested_scope: str
    caveat_state: str
    validity_state: str
    admission_status: Literal[
        "admitted_review_only", "admitted_caveated", "admitted_bounded_exchange",
        "admitted_baseline_support", "blocked_invalid", "blocked_expired",
        "blocked_scope_mismatch", "blocked_source_unhealthy", "blocked_by_sovereignty"
    ]
    warnings: List[str] = Field(default_factory=list)

class HubRoutingDecisionRecord(BaseModel):
    decision_id: str
    admission_ref: str
    routing_outcome: Literal[
        "route_review_only", "route_bounded_exchange", "route_baseline_support_only",
        "route_caveated_visibility", "queue_for_validation", "block_and_quarantine",
        "reroute_to_internal_only"
    ]
    applied_caveats: List[str]
    explanation: str

class BaselineCatalogEntryRecord(BaseModel):
    baseline_entry_id: str
    baseline_ref: str
    baseline_family: Literal[
        "treaty_baseline_catalog", "continuity_baseline_catalog",
        "translation_integrity_baseline_catalog", "sovereignty_respect_baseline_catalog",
        "replay_requirements_baseline_catalog", "rollback_visibility_baseline_catalog",
        "benchmark_preview_catalog"
    ]
    supported_treaty_families: List[str]
    supported_dimension_refs: List[str]
    baseline_version_ref: str
    freshness_state: str
    discoverability_state: Literal[
        "discoverable_current", "discoverable_caveated", "discoverable_review_only",
        "discoverable_stale", "hidden_superseded", "hidden_expired", "hidden_scope_limited"
    ]
    caveat_summary: str
    warnings: List[str] = Field(default_factory=list)

class TreatyBaselineCatalogRecord(BaseModel):
    catalog_id: str
    entries: List[BaselineCatalogEntryRecord]
    catalog_family: str
    health_status: str
    warnings: List[str] = Field(default_factory=list)

class SovereignPolicyAttestationEcosystemRecord(BaseModel):
    ecosystem_id: str
    ecosystem_family: str
    participant_refs: List[str]
    hub_refs: List[str]
    registry_refs: List[str]
    baseline_catalog_refs: List[str]
    supported_attestation_families: List[str]
    participation_policy_ref: str
    health_status: str
    warnings: List[str] = Field(default_factory=list)

class EcosystemParticipantRecord(BaseModel):
    participant_id: str
    participant_family: Literal[
        "corridor_registry_participant", "attestation_issuer_participant",
        "treaty_baseline_catalog_participant", "conformance_pack_participant",
        "review_observer_participant", "internal_preview_participant",
        "bounded_exchange_participant"
    ]
    source_registry_refs: List[str]
    issuer_profile_refs: List[str]
    supported_attestation_families: List[str]
    supported_exchange_scopes: List[str]
    visibility_profile: str
    participation_status: Literal[
        "participating_internal", "participating_review_only",
        "participating_bounded_exchange", "participating_caveated",
        "participating_suspended", "participating_expired", "participating_removed"
    ]
    warnings: List[str] = Field(default_factory=list)

class IssuerCapabilityRecord(BaseModel):
    supported_attestation_families: List[str]
    max_scope_class: str
    caveat_handling_support: bool
    validity_window_support: bool
    exchange_scope_support: bool
    replay_evidence_support: bool
    degraded_exchange_support: bool
    sovereignty_override_support: bool = False

class PolicyAttestationProfileRecord(BaseModel):
    supported_dimensions: List[str]
    supported_caveat_classes: List[str]
    exchange_visibility: Literal[
        "internal_only", "review_only", "bounded_exchange_visible",
        "catalog_visible_only", "baseline_visible_only",
        "hidden_due_to_sovereignty", "hidden_due_to_health"
    ]
    benchmark_attachment_support: bool
    conformance_pack_linkage_support: bool
    registry_projection_support: bool
