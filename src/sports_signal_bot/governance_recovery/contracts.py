from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum
from datetime import datetime

class ExceptionEntryProjectionStatus(str, Enum):
    PROJECTED_CURRENT_EXCEPTION = "projected_current_exception"
    PROJECTED_CAVEATED_EXCEPTION = "projected_caveated_exception"
    PROJECTED_REVIEW_ONLY_EXCEPTION = "projected_review_only_exception"
    PROJECTED_EXPIRING_EXCEPTION = "projected_expiring_exception"
    PROJECTED_EXPIRED_EXCEPTION = "projected_expired_exception"
    PROJECTED_SUPERSEDED_EXCEPTION = "projected_superseded_exception"
    PROJECTED_BLOCKED_EXCEPTION = "projected_blocked_exception"

class ExceptionFederationHealthRecord(BaseModel):
    is_healthy: bool
    stale_count: int = 0
    expired_count: int = 0
    superseded_count: int = 0
    blocked_count: int = 0

class ExceptionFederationWarningRecord(BaseModel):
    warning_id: str
    message: str
    severity: str

class ExceptionRegistryFederationRecord(BaseModel):
    exception_federation_id: str
    federation_family: str
    member_exception_registry_refs: List[str] = Field(default_factory=list)
    active_link_refs: List[str] = Field(default_factory=list)
    currentness_policy_ref: str
    expiry_policy_ref: str
    supersession_policy_ref: str
    health_status: ExceptionFederationHealthRecord
    warnings: List[ExceptionFederationWarningRecord] = Field(default_factory=list)

class FederatedExceptionRegistryNodeRecord(BaseModel):
    node_id: str
    exception_registry_ref: str
    supported_exception_families: List[str] = Field(default_factory=list)
    current_pointer_state: str
    freshness_state: str
    expiry_state: str
    visibility_profile: str
    warnings: List[ExceptionFederationWarningRecord] = Field(default_factory=list)

class ExceptionFederationLinkRecord(BaseModel):
    link_id: str
    source_node_ref: str
    target_node_ref: str

class ExceptionFederationCurrentnessRecord(BaseModel):
    exception_ref: str
    is_current: bool

class ExceptionFederationExpiryRecord(BaseModel):
    exception_ref: str
    is_expired: bool

class ExceptionFederationSupersessionRecord(BaseModel):
    exception_ref: str
    is_superseded: bool
    successor_ref: Optional[str] = None

class ExceptionFederationVisibilityRecord(BaseModel):
    exception_ref: str
    projection_status: ExceptionEntryProjectionStatus

class ExceptionFederationManifestRecord(BaseModel):
    manifest_id: str
    generated_at: datetime
    federation_ref: str

class EdgeStatus(str, Enum):
    ROUTE_EDGE_CURRENT = "route_edge_current"
    ROUTE_EDGE_CAVEATED = "route_edge_caveated"
    ROUTE_EDGE_REVIEW_ONLY = "route_edge_review_only"
    ROUTE_EDGE_DEGRADED = "route_edge_degraded"
    ROUTE_EDGE_BACKPRESSURED = "route_edge_backpressured"
    ROUTE_EDGE_BLOCKED = "route_edge_blocked"
    ROUTE_EDGE_EXPIRED = "route_edge_expired"
    ROUTE_EDGE_SUPERSEDED = "route_edge_superseded"

class RoutingPathOutcome(str, Enum):
    BOUNDED_GOVERNANCE_PATH = "bounded_governance_path"
    REVIEW_ONLY_PATH = "review_only_path"
    CAVEATED_PATH = "caveated_path"
    DEGRADED_FALLBACK_PATH = "degraded_fallback_path"
    REPLAY_REQUIRED_PATH = "replay_required_path"
    BLOCKED_PATH = "blocked_path"
    NO_SAFE_QUORUM_PATH = "no_safe_quorum_path"

class RoutingPressureState(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"
    SUPPRESS_NONCRITICAL_QUORUM_ROUTES = "suppress_noncritical_quorum_routes"

class QuorumRoutingHealthRecord(BaseModel):
    is_healthy: bool
    degraded_edge_count: int = 0
    blocked_edge_count: int = 0

class QuorumRoutingWarningRecord(BaseModel):
    warning_id: str
    message: str

class QuorumExchangeRoutingFabricRecord(BaseModel):
    quorum_routing_fabric_id: str
    fabric_family: str
    node_refs: List[str] = Field(default_factory=list)
    edge_refs: List[str] = Field(default_factory=list)
    routing_policy_ref: str
    pressure_policy_ref: str
    degradation_policy_ref: str
    health_status: QuorumRoutingHealthRecord
    warnings: List[QuorumRoutingWarningRecord] = Field(default_factory=list)

class QuorumRoutingNodeRecord(BaseModel):
    node_id: str

class QuorumRoutingEdgeRecord(BaseModel):
    edge_id: str
    source_node_ref: str
    target_node_ref: str
    supported_quorum_exchange_families: List[str] = Field(default_factory=list)
    supported_scope_classes: List[str] = Field(default_factory=list)
    currentness_state: str
    caveat_transfer_policy: str
    sovereignty_constraints: List[str] = Field(default_factory=list)
    edge_status: EdgeStatus
    warnings: List[QuorumRoutingWarningRecord] = Field(default_factory=list)

class QuorumRoutingPathRecord(BaseModel):
    path_id: str
    edge_refs: List[str]
    outcome: RoutingPathOutcome

class QuorumRoutingDecisionRecord(BaseModel):
    decision_id: str
    path_ref: str
    outcome: RoutingPathOutcome

class QuorumRoutingConstraintRecord(BaseModel):
    constraint_id: str
    constraint_type: str

class QuorumRoutingPressureRecord(BaseModel):
    pressure_id: str
    stale_packet_density: float
    replay_backlog: int
    degraded_edge_ratio: float
    caveat_heavy_path_ratio: float
    exception_burden: float
    successor_resolution_backlog: int
    controller_alert_density: float
    audit_replay_load: float
    state: RoutingPressureState

class QuorumRoutingManifestRecord(BaseModel):
    manifest_id: str
    fabric_ref: str

class SuccessorStatus(str, Enum):
    SUCCESSOR_RESOLVED_CURRENT = "successor_resolved_current"
    SUCCESSOR_RESOLVED_CAVEATED = "successor_resolved_caveated"
    SUCCESSOR_REVIEW_ONLY = "successor_review_only"
    SUCCESSOR_UNRESOLVED = "successor_unresolved"
    SUCCESSOR_STALE = "successor_stale"
    SUCCESSOR_SUPERSEDED = "successor_superseded"
    SUCCESSOR_BLOCKED = "successor_blocked"

class SuccessorRegistryHealthRecord(BaseModel):
    is_healthy: bool
    unresolved_count: int = 0
    stale_count: int = 0

class SuccessorRegistryWarningRecord(BaseModel):
    warning_id: str
    message: str

class BaselineSuccessorRegistryRecord(BaseModel):
    successor_registry_id: str
    registry_family: str
    tracked_baseline_refs: List[str] = Field(default_factory=list)
    successor_link_refs: List[str] = Field(default_factory=list)
    current_successor_refs: List[str] = Field(default_factory=list)
    unresolved_successor_refs: List[str] = Field(default_factory=list)
    replay_refs: List[str] = Field(default_factory=list)
    health_status: SuccessorRegistryHealthRecord
    warnings: List[SuccessorRegistryWarningRecord] = Field(default_factory=list)

class SuccessorRegistryEntryRecord(BaseModel):
    successor_entry_id: str
    source_baseline_ref: str
    candidate_successor_refs: List[str] = Field(default_factory=list)
    selected_successor_ref: Optional[str] = None
    successor_status: SuccessorStatus
    applicability_scope: str
    freshness_state: str
    warnings: List[SuccessorRegistryWarningRecord] = Field(default_factory=list)

class SuccessorLinkRecord(BaseModel):
    link_id: str
    source_ref: str
    target_ref: str

class SuccessorChainRecord(BaseModel):
    chain_id: str
    source_baseline_ref: str
    successor_sequence: List[str] = Field(default_factory=list)
    resolution_evidence_refs: List[str] = Field(default_factory=list)
    applicability_deltas: Dict[str, Any] = Field(default_factory=dict)
    freshness_deltas: Dict[str, Any] = Field(default_factory=dict)
    caveat_deltas: Dict[str, Any] = Field(default_factory=dict)
    supersession_reasons: Dict[str, str] = Field(default_factory=dict)
    replay_support_refs: List[str] = Field(default_factory=list)

class SuccessorResolutionRecord(BaseModel):
    resolution_id: str
    entry_ref: str
    resolved_successor_ref: str

class SuccessorApplicabilityRecord(BaseModel):
    applicability_id: str
    scope: str

class SuccessorVisibilityRecord(BaseModel):
    visibility_id: str
    status: SuccessorStatus

class SuccessorReplayRecord(BaseModel):
    replay_id: str
    entry_ref: str

class SuccessorRegistryManifestRecord(BaseModel):
    manifest_id: str
    registry_ref: str

class EscalationStage(str, Enum):
    MONITORING = "monitoring"
    CAUTION = "caution"
    REVIEW_BIAS = "review_bias"
    REPLAY_REQUIRED = "replay_required"
    SUCCESSOR_RESOLUTION_REQUIRED = "successor_resolution_required"
    EXCEPTION_REDUCTION_REQUIRED = "exception_reduction_required"
    DEGRADED_RECOVERY = "degraded_recovery"
    BLOCKED_RECOVERY = "blocked_recovery"
    STABILIZED = "stabilized"

class EscalationDecisionType(str, Enum):
    SHIFT_TO_REVIEW_ONLY_BIAS = "shift_to_review_only_bias"
    REQUIRE_REPLAY_BEFORE_PROJECTION = "require_replay_before_projection"
    REQUIRE_SUCCESSOR_RESOLUTION = "require_successor_resolution"
    SUPPRESS_NONCRITICAL_QUORUM_PATHS = "suppress_noncritical_quorum_paths"
    CAP_STRONG_GOVERNANCE_HINTS = "cap_strong_governance_hints"
    PRESERVE_NO_SAFE_HINT = "preserve_no_safe_hint"
    EXPIRE_OR_REOPEN_EXCEPTION = "expire_or_reopen_exception"
    MARK_RECOVERY_BLOCKED = "mark_recovery_blocked"
    RESTORE_CAVEATED_BOUNDED_HINT = "restore_caveated_bounded_hint"

class EscalationHealthRecord(BaseModel):
    is_healthy: bool
    current_stage: EscalationStage

class EscalationWarningRecord(BaseModel):
    warning_id: str
    message: str

class GovernanceRecoveryEscalatorRecord(BaseModel):
    escalator_id: str
    escalator_family: str
    monitored_scope_refs: List[str] = Field(default_factory=list)
    trigger_refs: List[str] = Field(default_factory=list)
    stage_refs: List[str] = Field(default_factory=list)
    checkpoint_refs: List[str] = Field(default_factory=list)
    recovery_policy_ref: str
    current_state: EscalationStage
    health_status: EscalationHealthRecord
    warnings: List[EscalationWarningRecord] = Field(default_factory=list)

class EscalationStageRecord(BaseModel):
    stage_id: str
    stage_family: EscalationStage
    precedence_rank: int
    entry_conditions: List[str] = Field(default_factory=list)
    output_effects: List[str] = Field(default_factory=list)
    exit_conditions: List[str] = Field(default_factory=list)
    rollback_or_recovery_notes: str
    warnings: List[EscalationWarningRecord] = Field(default_factory=list)

class EscalationTriggerRecord(BaseModel):
    trigger_id: str
    trigger_type: str

class EscalationCheckpointRecord(BaseModel):
    checkpoint_id: str
    passed: bool

class EscalationDecisionRecord(BaseModel):
    decision_id: str
    decision_type: EscalationDecisionType

class EscalationRecoveryPathRecord(BaseModel):
    path_id: str
    decisions: List[EscalationDecisionRecord] = Field(default_factory=list)

class EscalationBoundRecord(BaseModel):
    bound_id: str
    bound_type: str

class EscalationManifestRecord(BaseModel):
    manifest_id: str
    escalator_ref: str
