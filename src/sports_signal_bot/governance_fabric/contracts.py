import datetime
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

# --- COUNCIL CONTRACTS ---
class CouncilTierRecord(BaseModel):
    tier_id: str
    tier_level: int
    tier_family: str

class GovernanceTierCouncilRecord(BaseModel):
    council_id: str
    council_family: str
    governed_tier_refs: List[str]
    participant_refs: List[str]
    quorum_policy_ref: str
    precedence_policy_ref: str
    backlog_ref: str
    health_status: str
    warnings: List[str]

class CouncilCaseRecordV2(BaseModel):
    case_id: str
    case_family: str
    input_scope_ref: str
    input_route_refs: Optional[List[str]] = []
    input_overlay_refs: Optional[List[str]] = []
    input_signal_refs: Optional[List[str]] = []
    input_baseline_refs: Optional[List[str]] = []
    decision_needed: str
    escalation_state: str
    case_status: str
    warnings: List[str]

class CouncilParticipantRecordV2(BaseModel):
    participant_id: str
    role: str
    weight: float

class CouncilDecisionEnvelopeRecord(BaseModel):
    decision_id: str
    case_ref: str
    decision_type: str
    caveats: List[str]
    lineage_refs: List[str]

class CouncilVoteRecordV2(BaseModel):
    vote_id: str
    participant_ref: str
    case_ref: str
    position: str

class CouncilQuorumRecord(BaseModel):
    quorum_id: str
    case_ref: str
    quorum_type: str
    met: bool
    details: str

class CouncilPrecedenceRecordV2(BaseModel):
    precedence_id: str
    policy_name: str
    rules: Dict[str, str]

class CouncilEscalationRecord(BaseModel):
    escalation_id: str
    case_ref: str
    trigger_reason: str
    escalation_outcome: str

class CouncilBacklogRecord(BaseModel):
    backlog_id: str
    pending_case_refs: List[str]

class CouncilHealthRecordV2(BaseModel):
    health_id: str
    council_ref: str
    quorum_success_rate: float
    backlog_size: int
    status: str

# --- FABRIC CONTRACTS ---

class FabricSegmentRecord(BaseModel):
    segment_id: str
    segment_family: str
    participating_layer_refs: List[str]
    participating_member_refs: List[str]
    scope_constraints: List[str]
    freshness_policy_ref: str
    suppression_policy_ref: str
    segment_status: str
    warnings: List[str]

class FabricChannelRecord(BaseModel):
    channel_id: str
    source_segment_ref: str
    target_segment_ref: str
    supported_signal_families: List[str]
    supported_scope_classes: List[str]
    pressure_state: str
    freshness_state: str
    channel_status: str
    caveat_transfer_policy: str
    warnings: List[str]

class FabricSignalPacketRecord(BaseModel):
    packet_id: str
    signal_family: str
    content: str
    provenance_chain: List[str]

class FabricSuppressionRecord(BaseModel):
    suppression_id: str
    target_ref: str
    reason: str

class FabricCorroborationRecord(BaseModel):
    corroboration_id: str
    signal_refs: List[str]
    confidence_score: float

class ConsortiumSignalFabricRecord(BaseModel):
    signal_fabric_id: str
    fabric_family: str
    segment_refs: List[str]
    channel_refs: List[str]
    active_signal_packet_refs: List[str]
    suppression_refs: List[str]
    corroboration_refs: List[str]
    health_status: str
    warnings: List[str]

class FabricFlowRecord(BaseModel):
    flow_id: str
    input_signal_ref: str
    traversed_channel_refs: List[str]
    provenance_chain: List[str]
    freshness_decay: float
    corroboration_updates: List[str]
    suppression_events: List[str]
    projected_targets: List[str]
    final_signal_state: str

class FabricPressureRecordV2(BaseModel):
    pressure_id: str
    fabric_ref: str
    stale_signal_density: float
    duplicate_signal_burst: float
    conflicting_cluster_density: float
    degraded_channel_ratio: float
    corroboration_backlog: int
    suppression_burden: float
    provenance_gap_ratio: float
    controller_alert_density: float
    pressure_outcome: str

class FabricHealthRecordV2(BaseModel):
    health_id: str
    fabric_ref: str
    flow_success_rate: float
    status: str

# --- FEDERATION CONTRACTS ---

class FederatedBaselineRegistryNodeRecord(BaseModel):
    node_id: str
    baseline_registry_ref: str
    supported_baseline_families: List[str]
    current_pointer_state: str
    freshness_state: str
    applicability_scope: str
    visibility_profile: str
    warnings: List[str]

class BaselineFederationLinkRecord(BaseModel):
    link_id: str
    source_node_ref: str
    target_node_ref: str
    status: str

class BaselineFederationCurrentnessRecord(BaseModel):
    currentness_id: str
    source_current_pointer: str
    federated_current_projection: str
    successor_projection: str
    applicability_projection: str
    freshness_projection: str
    replay_need: bool
    caveat_burden: List[str]
    federation_drift_status: str
    currentness_outcome: str

class BaselineFederationApplicabilityRecord(BaseModel):
    applicability_id: str
    scope: str
    rules: Dict[str, str]

class BaselineFederationSupersessionRecord(BaseModel):
    supersession_id: str
    old_pointer: str
    new_pointer: str
    reason: str

class BaselineFederationDriftRecord(BaseModel):
    drift_id: str
    link_ref: str
    drift_amount: float
    drift_status: str

class BaselineRegistryFederationRecord(BaseModel):
    baseline_federation_id: str
    federation_family: str
    member_registry_refs: List[str]
    active_link_refs: List[str]
    currentness_policy_ref: str
    applicability_policy_ref: str
    supersession_policy_ref: str
    health_status: str
    warnings: List[str]

class BaselineFederationHealthRecord(BaseModel):
    health_id: str
    federation_ref: str
    currentness_match_rate: float
    status: str

# --- AUDIT EXCHANGES ---

class ProjectionAuditScopeRecord(BaseModel):
    scope_id: str
    boundaries: List[str]

class ProjectionAuditEvidenceRecord(BaseModel):
    evidence_id: str
    evidence_family: str
    content_ref: str

class ProjectionAuditPacketRecord(BaseModel):
    audit_packet_id: str
    source_projection_refs: List[str]
    source_overlay_refs: Optional[List[str]] = []
    source_signal_refs: Optional[List[str]] = []
    source_baseline_refs: Optional[List[str]] = []
    source_controller_refs: Optional[List[str]] = []
    preserved_caveat_refs: List[str]
    currentness_refs: List[str]
    projection_method_summary: str
    evidence_refs: List[str]
    validity_window: str
    audit_status: str
    warnings: List[str]

class ProjectionAuditEnvelopeRecord(BaseModel):
    envelope_id: str
    packet_ref: str
    signatures: List[str]

class ProjectionAuditReplayRecord(BaseModel):
    replay_id: str
    packet_ref: str
    replay_outcome: str
    drift_details: str

class ProjectionAuditVerificationRecord(BaseModel):
    verification_id: str
    packet_ref: str
    verifier_ref: str
    verification_status: str

class ProjectionAuditDecisionRecord(BaseModel):
    decision_id: str
    exchange_ref: str
    final_status: str
    applied_caps: List[str]

class SovereignProjectionAuditExchangeRecord(BaseModel):
    audit_exchange_id: str
    source_scope_ref: str
    target_scope_ref: str
    audit_packet_refs: List[str]
    exchange_scope: str
    replay_support_refs: List[str]
    verification_refs: List[str]
    decision_refs: List[str]
    health_status: str
    warnings: List[str]

# --- MANIFESTS AND WARNINGS ---

class GovernanceCouncilManifestRecord(BaseModel):
    manifest_id: str
    timestamp: str
    council_refs: List[str]

class GovernanceCouncilWarningRecord(BaseModel):
    warning_id: str
    message: str

class SignalFabricManifestRecord(BaseModel):
    manifest_id: str
    timestamp: str
    fabric_refs: List[str]

class SignalFabricWarningRecord(BaseModel):
    warning_id: str
    message: str

class BaselineRegistryFederationManifestRecord(BaseModel):
    manifest_id: str
    timestamp: str
    federation_refs: List[str]

class BaselineFederationWarningRecord(BaseModel):
    warning_id: str
    message: str

class ProjectionAuditManifestRecord(BaseModel):
    manifest_id: str
    timestamp: str
    exchange_refs: List[str]

class ProjectionAuditWarningRecord(BaseModel):
    warning_id: str
    message: str
