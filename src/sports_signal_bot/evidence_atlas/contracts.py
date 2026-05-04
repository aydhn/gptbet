import datetime
from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field

class NarrativeFederationLinkStatus(str, Enum):
    link_current = "link_current"
    link_caveated = "link_caveated"
    link_review_only = "link_review_only"
    link_degraded = "link_degraded"
    link_blocked = "link_blocked"
    link_expired = "link_expired"
    link_superseded = "link_superseded"

class NarrativeFederationOutputStatus(str, Enum):
    federated_narrative_current_with_caps = "federated_narrative_current_with_caps"
    federated_narrative_caveated = "federated_narrative_caveated"
    federated_narrative_review_only = "federated_narrative_review_only"
    federated_narrative_degraded = "federated_narrative_degraded"
    federated_narrative_blocked = "federated_narrative_blocked"
    federated_narrative_stale = "federated_narrative_stale"

class AssuranceMeshEdgeStatus(str, Enum):
    edge_current = "edge_current"
    edge_caveated = "edge_caveated"
    edge_review_only = "edge_review_only"
    edge_degraded = "edge_degraded"
    edge_backpressured = "edge_backpressured"
    edge_blocked = "edge_blocked"
    edge_expired = "edge_expired"
    edge_superseded = "edge_superseded"

class AssuranceMeshPathOutcome(str, Enum):
    bounded_assurance_path = "bounded_assurance_path"
    review_only_assurance_path = "review_only_assurance_path"
    caveated_assurance_path = "caveated_assurance_path"
    degraded_assurance_path = "degraded_assurance_path"
    blocked_assurance_path = "blocked_assurance_path"
    no_safe_assurance_path = "no_safe_assurance_path"

class AssuranceMeshPressureState(str, Enum):
    low = "low"
    moderate = "moderate"
    high = "high"
    critical = "critical"
    suppress_noncritical_assurance_paths = "suppress_noncritical_assurance_paths"
    review_only_bias = "review_only_bias"

class ReplayClearingCouncilCaseStatus(str, Enum):
    case_opened = "case_opened"
    case_collecting_evidence = "case_collecting_evidence"
    case_quorum_pending = "case_quorum_pending"
    case_decided = "case_decided"
    case_decided_with_caveats = "case_decided_with_caveats"
    case_review_only = "case_review_only"
    case_blocked = "case_blocked"
    case_superseded = "case_superseded"
    case_archived = "case_archived"

class ReplayClearingDecisionOutcome(str, Enum):
    preserve_existing_clearing_cap = "preserve_existing_clearing_cap"
    downgrade_to_review_only_clearing = "downgrade_to_review_only_clearing"
    require_replay_revalidation = "require_replay_revalidation"
    require_debt_reassessment = "require_debt_reassessment"
    require_offer_refresh = "require_offer_refresh"
    preserve_no_safe_replay_visibility = "preserve_no_safe_replay_visibility"
    accept_bounded_clearing_with_caveats = "accept_bounded_clearing_with_caveats"
    block_due_to_unresolved_clearing_conflict = "block_due_to_unresolved_clearing_conflict"


# -- NARRATIVE FEDERATION RECORDS --
class NarrativeCompilerFederationWarningRecord(BaseModel):
    warning_code: str
    message: str
    severity: str
    is_sovereignty_related: bool = False

class NarrativeFederationCurrentnessRecord(BaseModel):
    is_current: bool
    stale_sections: List[str] = Field(default_factory=list)
    last_refresh: datetime.datetime
    expires_at: datetime.datetime

class NarrativeFederationCaveatRecord(BaseModel):
    caveat_id: str
    description: str
    requires_no_safe_visibility: bool = False

class NarrativeFederationAudienceRecord(BaseModel):
    audience_profile: str
    restrictions: List[str] = Field(default_factory=list)

class NarrativeFederationDecisionRecord(BaseModel):
    decision_id: str
    outcome: str
    justification: str

class NarrativeFederationHealthRecord(BaseModel):
    is_healthy: bool
    score: float
    health_issues: List[str] = Field(default_factory=list)

class FederatedNarrativeNodeRecord(BaseModel):
    node_id: str
    narrative_compiler_ref: str
    narrative_family: str
    supported_audience_profiles: List[str] = Field(default_factory=list)
    currentness_state: NarrativeFederationCurrentnessRecord
    caveat_state: List[NarrativeFederationCaveatRecord] = Field(default_factory=list)
    sovereignty_state: str
    node_status: str
    warnings: List[NarrativeCompilerFederationWarningRecord] = Field(default_factory=list)

class NarrativeFederationLinkRecord(BaseModel):
    link_id: str
    source_node_ref: str
    target_node_ref: str
    status: NarrativeFederationLinkStatus
    caveats: List[NarrativeFederationCaveatRecord] = Field(default_factory=list)

class NarrativeCompilerFederationRecord(BaseModel):
    narrative_federation_id: str
    federation_family: str
    member_narrative_compiler_refs: List[str] = Field(default_factory=list)
    active_link_refs: List[str] = Field(default_factory=list)
    currentness_policy_ref: str
    audience_policy_ref: str
    caveat_policy_ref: str
    health_status: str
    warnings: List[NarrativeCompilerFederationWarningRecord] = Field(default_factory=list)

class NarrativeCompilerFederationManifestRecord(BaseModel):
    manifest_id: str
    federations: List[NarrativeCompilerFederationRecord] = Field(default_factory=list)
    generated_at: datetime.datetime

# -- ASSURANCE MESH RECORDS --
class AssuranceExchangeMeshWarningRecord(BaseModel):
    warning_code: str
    message: str
    severity: str
    is_sovereignty_related: bool = False

class AssuranceMeshConstraintRecord(BaseModel):
    constraint_id: str
    constraint_type: str

class AssuranceMeshPressureRecord(BaseModel):
    pressure_state: AssuranceMeshPressureState
    stale_packet_density: float
    backpressured_edge_ratio: float
    degraded_node_ratio: float
    narrative_refresh_backlog: int
    alert_density: float
    no_safe_visibility_burden: float
    audience_projection_mismatch: float
    caveat_heavy_packet_ratio: float

class AssuranceMeshDegradationRecord(BaseModel):
    is_degraded: bool
    degraded_paths: List[str] = Field(default_factory=list)

class AssuranceMeshHealthRecord(BaseModel):
    is_healthy: bool
    score: float
    health_issues: List[str] = Field(default_factory=list)

class AssuranceMeshNodeRecord(BaseModel):
    node_id: str
    node_family: str
    hosted_dashboard_exchange_refs: List[str] = Field(default_factory=list)
    hosted_narrative_refs: List[str] = Field(default_factory=list)
    supported_scope_classes: List[str] = Field(default_factory=list)
    currentness_state: str
    node_status: str
    warnings: List[AssuranceExchangeMeshWarningRecord] = Field(default_factory=list)

class AssuranceMeshEdgeRecord(BaseModel):
    edge_id: str
    source_node_ref: str
    target_node_ref: str
    supported_exchange_families: List[str] = Field(default_factory=list)
    supported_scope_classes: List[str] = Field(default_factory=list)
    caveat_transfer_policy: str
    currentness_state: str
    edge_status: AssuranceMeshEdgeStatus
    warnings: List[AssuranceExchangeMeshWarningRecord] = Field(default_factory=list)

class AssuranceMeshPathRecord(BaseModel):
    path_id: str
    node_sequence: List[str] = Field(default_factory=list)
    edge_sequence: List[str] = Field(default_factory=list)
    outcome: AssuranceMeshPathOutcome

class AssuranceMeshPacketRecord(BaseModel):
    packet_id: str
    payload_ref: str
    path_ref: str

class AssuranceExchangeMeshRecord(BaseModel):
    assurance_mesh_id: str
    mesh_family: str
    node_refs: List[str] = Field(default_factory=list)
    edge_refs: List[str] = Field(default_factory=list)
    packet_refs: List[str] = Field(default_factory=list)
    routing_policy_ref: str
    pressure_policy_ref: str
    degradation_policy_ref: str
    health_status: str
    warnings: List[AssuranceExchangeMeshWarningRecord] = Field(default_factory=list)

class AssuranceExchangeMeshManifestRecord(BaseModel):
    manifest_id: str
    meshes: List[AssuranceExchangeMeshRecord] = Field(default_factory=list)
    generated_at: datetime.datetime

# -- REPLAY CLEARING COUNCIL RECORDS --
class ReplayClearingCouncilWarningRecord(BaseModel):
    warning_code: str
    message: str
    severity: str
    is_sovereignty_related: bool = False

class ReplayClearingCouncilInputRecord(BaseModel):
    input_id: str
    input_type: str

class ReplayClearingCouncilEvidenceRecord(BaseModel):
    evidence_id: str
    evidence_type: str

class ReplayClearingCouncilVoteRecord(BaseModel):
    vote_id: str
    voter_ref: str
    vote_value: str

class ReplayClearingCouncilDecisionRecord(BaseModel):
    decision_id: str
    outcome: ReplayClearingDecisionOutcome
    justification: str

class ReplayClearingCouncilCapRecord(BaseModel):
    cap_id: str
    cap_value: str

class ReplayClearingCouncilBacklogRecord(BaseModel):
    backlog_id: str
    case_refs: List[str] = Field(default_factory=list)

class ReplayClearingCouncilHealthRecord(BaseModel):
    is_healthy: bool
    score: float

class ReplayClearingCouncilCaseRecord(BaseModel):
    replay_clearing_case_id: str
    case_family: str
    input_clearing_refs: List[str] = Field(default_factory=list)
    input_market_offer_refs: List[str] = Field(default_factory=list)
    input_market_request_refs: List[str] = Field(default_factory=list)
    input_debt_refs: List[str] = Field(default_factory=list)
    input_sovereignty_refs: List[str] = Field(default_factory=list)
    decision_needed: str
    escalation_state: str
    case_status: ReplayClearingCouncilCaseStatus
    warnings: List[ReplayClearingCouncilWarningRecord] = Field(default_factory=list)

class ReplayClearingCouncilRecord(BaseModel):
    replay_clearing_council_id: str
    council_family: str
    governed_clearing_layer_refs: List[str] = Field(default_factory=list)
    participant_refs: List[str] = Field(default_factory=list)
    quorum_policy_ref: str
    precedence_policy_ref: str
    backlog_ref: str
    health_status: str
    warnings: List[ReplayClearingCouncilWarningRecord] = Field(default_factory=list)

class ReplayClearingCouncilManifestRecord(BaseModel):
    manifest_id: str
    councils: List[ReplayClearingCouncilRecord] = Field(default_factory=list)
    generated_at: datetime.datetime


# -- EVIDENCE ATLAS RECORDS --
class GovernanceEvidenceAtlasWarningRecord(BaseModel):
    warning_code: str
    message: str
    severity: str
    is_sovereignty_related: bool = False

class EvidenceAtlasFreshnessRecord(BaseModel):
    is_fresh: bool
    last_verified: datetime.datetime

class EvidenceAtlasHealthRecord(BaseModel):
    is_healthy: bool
    score: float
    stale_node_count: int
    stale_edge_count: int

class EvidenceAtlasNodeRecord(BaseModel):
    atlas_node_id: str
    node_family: str
    source_ref: str
    source_family: str
    currentness_state: str
    applicability_scope: str
    caveat_state: str
    warnings: List[GovernanceEvidenceAtlasWarningRecord] = Field(default_factory=list)

class EvidenceAtlasEdgeRecord(BaseModel):
    atlas_edge_id: str
    source_node_ref: str
    target_node_ref: str
    relationship_family: str
    freshness_state: str
    caveat_transfer_policy: str
    edge_status: str
    warnings: List[GovernanceEvidenceAtlasWarningRecord] = Field(default_factory=list)

class EvidenceAtlasViewRecord(BaseModel):
    view_id: str
    view_family: str
    node_refs: List[str] = Field(default_factory=list)

class EvidenceAtlasLayerRecord(BaseModel):
    layer_id: str
    layer_family: str

class EvidenceAtlasQueryRecord(BaseModel):
    query_id: str
    query_family: str
    query_params: Dict[str, Any] = Field(default_factory=dict)
    results_caveated: bool = False
    results_stale: bool = False

class EvidenceAtlasMatchRecord(BaseModel):
    match_id: str
    node_ref: str

class SovereignGovernanceEvidenceAtlasRecord(BaseModel):
    evidence_atlas_id: str
    atlas_family: str
    node_refs: List[str] = Field(default_factory=list)
    edge_refs: List[str] = Field(default_factory=list)
    layer_refs: List[str] = Field(default_factory=list)
    view_refs: List[str] = Field(default_factory=list)
    freshness_policy_ref: str
    health_status: str
    warnings: List[GovernanceEvidenceAtlasWarningRecord] = Field(default_factory=list)

class GovernanceEvidenceAtlasManifestRecord(BaseModel):
    manifest_id: str
    atlases: List[SovereignGovernanceEvidenceAtlasRecord] = Field(default_factory=list)
    generated_at: datetime.datetime
