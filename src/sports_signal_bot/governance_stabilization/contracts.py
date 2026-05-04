from enum import Enum
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
import datetime

# --- TAXONOMIES ---

class RecoveryMeshFamily(str, Enum):
    review_only_recovery_mesh = "review_only_recovery_mesh"
    bounded_recovery_mesh = "bounded_recovery_mesh"
    successor_resolution_mesh = "successor_resolution_mesh"
    exception_burden_recovery_mesh = "exception_burden_recovery_mesh"
    replay_recovery_mesh = "replay_recovery_mesh"
    degraded_recovery_mesh = "degraded_recovery_mesh"
    stabilization_support_mesh = "stabilization_support_mesh"

class RecoveryMeshNodeFamily(str, Enum):
    quorum_source_node = "quorum_source_node"
    replay_validation_node = "replay_validation_node"
    successor_resolution_node = "successor_resolution_node"
    exception_lineage_node = "exception_lineage_node"
    stabilization_observer_node = "stabilization_observer_node"
    degraded_fallback_node = "degraded_fallback_node"
    review_bias_node = "review_bias_node"
    sovereignty_guard_node = "sovereignty_guard_node"

class RecoveryEdgeStatus(str, Enum):
    edge_current = "edge_current"
    edge_caveated = "edge_caveated"
    edge_review_only = "edge_review_only"
    edge_degraded = "edge_degraded"
    edge_backpressured = "edge_backpressured"
    edge_blocked = "edge_blocked"
    edge_expired = "edge_expired"
    edge_superseded = "edge_superseded"

class RecoveryQuorumStrength(str, Enum):
    bounded_recovery_quorum = "bounded_recovery_quorum"
    replay_guard_quorum = "replay_guard_quorum"
    successor_resolution_quorum = "successor_resolution_quorum"
    lineage_consistency_quorum = "lineage_consistency_quorum"
    stabilization_readiness_quorum = "stabilization_readiness_quorum"
    sovereignty_guard_quorum = "sovereignty_guard_quorum"
    degraded_recovery_quorum = "degraded_recovery_quorum"

class RecoveryPathOutcome(str, Enum):
    bounded_recovery_hint = "bounded_recovery_hint"
    caveated_bounded_recovery_hint = "caveated_bounded_recovery_hint"
    review_only_recovery_hint = "review_only_recovery_hint"
    replay_required_recovery_hint = "replay_required_recovery_hint"
    successor_resolution_required_hint = "successor_resolution_required_hint"
    degraded_fallback_recovery_hint = "degraded_fallback_recovery_hint"
    blocked_recovery_hint = "blocked_recovery_hint"
    no_safe_recovery_hint = "no_safe_recovery_hint"

class RecoveryPressureState(str, Enum):
    low = "low"
    moderate = "moderate"
    high = "high"
    critical = "critical"
    suppress_noncritical_recovery_paths = "suppress_noncritical_recovery_paths"
    review_only_bias = "review_only_bias"

class SuccessorCouncilFamily(str, Enum):
    federated_successor_currentness_council = "federated_successor_currentness_council"
    successor_applicability_alignment_council = "successor_applicability_alignment_council"
    successor_visibility_council = "successor_visibility_council"
    successor_drift_resolution_council = "successor_drift_resolution_council"
    successor_replay_resolution_council = "successor_replay_resolution_council"
    sovereignty_bound_successor_council = "sovereignty_bound_successor_council"
    successor_stabilization_council = "successor_stabilization_council"

class SuccessorCaseFamily(str, Enum):
    successor_pointer_conflict_case = "successor_pointer_conflict_case"
    successor_applicability_mismatch_case = "successor_applicability_mismatch_case"
    missing_successor_visibility_case = "missing_successor_visibility_case"
    stale_successor_case = "stale_successor_case"
    successor_replay_divergence_case = "successor_replay_divergence_case"
    sovereignty_successor_case = "sovereignty_successor_case"
    successor_chain_fragment_case = "successor_chain_fragment_case"

class SuccessorCaseStatus(str, Enum):
    case_opened = "case_opened"
    case_collecting_evidence = "case_collecting_evidence"
    case_quorum_pending = "case_quorum_pending"
    case_converging = "case_converging"
    case_decided = "case_decided"
    case_decided_with_caveats = "case_decided_with_caveats"
    case_review_only = "case_review_only"
    case_blocked = "case_blocked"
    case_superseded = "case_superseded"
    case_archived = "case_archived"

class SuccessorCouncilDecision(str, Enum):
    preserve_caveated_successor_projection = "preserve_caveated_successor_projection"
    require_successor_chain_resolution = "require_successor_chain_resolution"
    downgrade_to_review_only_successor_hint = "downgrade_to_review_only_successor_hint"
    require_replay_before_successor_selection = "require_replay_before_successor_selection"
    suppress_stale_successor_projection = "suppress_stale_successor_projection"
    accept_bounded_successor_hint_with_caveats = "accept_bounded_successor_hint_with_caveats"
    preserve_local_successor_priority = "preserve_local_successor_priority"
    mark_unresolved_successor_block = "mark_unresolved_successor_block"

class SuccessorConvergenceBand(str, Enum):
    no_convergence = "no_convergence"
    weak_convergence = "weak_convergence"
    bounded_convergence = "bounded_convergence"
    strong_convergence_with_caveats = "strong_convergence_with_caveats"
    stable_convergence = "stable_convergence"

class ExceptionLineageRegistryFamily(str, Enum):
    sovereign_exception_lineage_registry = "sovereign_exception_lineage_registry"
    replay_required_exception_lineage_registry = "replay_required_exception_lineage_registry"
    successor_pending_exception_lineage_registry = "successor_pending_exception_lineage_registry"
    degraded_hint_exception_lineage_registry = "degraded_hint_exception_lineage_registry"
    review_only_exception_lineage_registry = "review_only_exception_lineage_registry"
    audit_rebuild_exception_lineage_registry = "audit_rebuild_exception_lineage_registry"
    stabilization_program_exception_lineage_registry = "stabilization_program_exception_lineage_registry"

class ExceptionLineageEntryStatus(str, Enum):
    lineage_current = "lineage_current"
    lineage_caveated = "lineage_caveated"
    lineage_review_only = "lineage_review_only"
    lineage_expiring = "lineage_expiring"
    lineage_expired = "lineage_expired"
    lineage_superseded = "lineage_superseded"
    lineage_replayed = "lineage_replayed"
    lineage_blocked = "lineage_blocked"

class StabilizationProgramFamily(str, Enum):
    quorum_stabilization_program = "quorum_stabilization_program"
    successor_resolution_stabilization_program = "successor_resolution_stabilization_program"
    exception_burden_stabilization_program = "exception_burden_stabilization_program"
    routing_pressure_stabilization_program = "routing_pressure_stabilization_program"
    replay_rebuild_stabilization_program = "replay_rebuild_stabilization_program"
    sovereignty_preservation_stabilization_program = "sovereignty_preservation_stabilization_program"
    degraded_governance_stabilization_program = "degraded_governance_stabilization_program"

class StabilizationStage(str, Enum):
    monitoring = "monitoring"
    caution = "caution"
    recovery_bias = "recovery_bias"
    replay_rebuild = "replay_rebuild"
    successor_resolution = "successor_resolution"
    exception_burden_reduction = "exception_burden_reduction"
    degraded_stabilization = "degraded_stabilization"
    blocked_stabilization = "blocked_stabilization"
    stabilized = "stabilized"
    regression_watch = "regression_watch"

class StabilizationCheckpointFamily(str, Enum):
    quorum_freshness_restored_checkpoint = "quorum_freshness_restored_checkpoint"
    successor_chain_resolved_checkpoint = "successor_chain_resolved_checkpoint"
    exception_burden_reduced_checkpoint = "exception_burden_reduced_checkpoint"
    replay_mismatch_cleared_checkpoint = "replay_mismatch_cleared_checkpoint"
    degraded_path_ratio_reduced_checkpoint = "degraded_path_ratio_reduced_checkpoint"
    lineage_gap_closed_checkpoint = "lineage_gap_closed_checkpoint"
    no_safe_hint_visibility_preserved_checkpoint = "no_safe_hint_visibility_preserved_checkpoint"
    sovereignty_constraints_preserved_checkpoint = "sovereignty_constraints_preserved_checkpoint"
    bounded_hint_restored_checkpoint = "bounded_hint_restored_checkpoint"

class StabilizationDecision(str, Enum):
    shift_to_recovery_bias = "shift_to_recovery_bias"
    require_replay_rebuild = "require_replay_rebuild"
    require_successor_resolution = "require_successor_resolution"
    require_exception_burden_reduction = "require_exception_burden_reduction"
    preserve_review_only_bias = "preserve_review_only_bias"
    preserve_no_safe_hint = "preserve_no_safe_hint"
    restore_caveated_bounded_hint = "restore_caveated_bounded_hint"
    mark_stabilization_blocked = "mark_stabilization_blocked"
    enter_regression_watch = "enter_regression_watch"

# --- RECORDS & MODELS ---

class RecoveryMeshNodeRecord(BaseModel):
    node_id: str
    node_family: RecoveryMeshNodeFamily
    supported_recovery_families: List[RecoveryMeshFamily] = Field(default_factory=list)
    currentness_state: str = "current"
    replay_state: str = "verified"
    burden_state: str = "nominal"
    node_status: str = "healthy"
    warnings: List[str] = Field(default_factory=list)

class RecoveryMeshEdgeRecord(BaseModel):
    edge_id: str
    source_node_ref: str
    target_node_ref: str
    supported_scope_classes: List[str] = Field(default_factory=list)
    supported_recovery_families: List[RecoveryMeshFamily] = Field(default_factory=list)
    caveat_transfer_policy: str = "preserve_all"
    sovereignty_constraints: List[str] = Field(default_factory=list)
    edge_status: RecoveryEdgeStatus
    warnings: List[str] = Field(default_factory=list)

class RecoveryMeshPressureRecord(BaseModel):
    stale_currentness_density: float = 0.0
    replay_backlog: int = 0
    unresolved_successor_density: float = 0.0
    exception_burden: float = 0.0
    degraded_edge_ratio: float = 0.0
    council_backlog: int = 0
    stabilization_alert_density: float = 0.0
    lineage_gap_ratio: float = 0.0
    pressure_state: RecoveryPressureState = RecoveryPressureState.low

class RecoveryMeshPathRecord(BaseModel):
    path_id: str
    nodes: List[str]
    edges: List[str]
    outcome: RecoveryPathOutcome
    caveats: List[str] = Field(default_factory=list)

class RecoveryQuorumMeshRecord(BaseModel):
    recovery_mesh_id: str
    mesh_family: RecoveryMeshFamily
    node_refs: List[RecoveryMeshNodeRecord] = Field(default_factory=list)
    edge_refs: List[RecoveryMeshEdgeRecord] = Field(default_factory=list)
    paths: List[RecoveryMeshPathRecord] = Field(default_factory=list)
    pressure: Optional[RecoveryMeshPressureRecord] = None
    quorum_policy_ref: str = "default_quorum_policy"
    fallback_policy_ref: str = "default_fallback_policy"
    health_status: str = "healthy"
    warnings: List[str] = Field(default_factory=list)

class SuccessorFederationCaseRecord(BaseModel):
    successor_case_id: str
    case_family: SuccessorCaseFamily
    source_baseline_refs: List[str] = Field(default_factory=list)
    candidate_successor_refs: List[str] = Field(default_factory=list)
    lineage_refs: List[str] = Field(default_factory=list)
    applicability_refs: List[str] = Field(default_factory=list)
    replay_requirement: str = "mandatory"
    convergence_state: SuccessorConvergenceBand = SuccessorConvergenceBand.no_convergence
    case_status: SuccessorCaseStatus = SuccessorCaseStatus.case_opened
    decision: Optional[SuccessorCouncilDecision] = None
    warnings: List[str] = Field(default_factory=list)

class SuccessorFederationCouncilRecord(BaseModel):
    successor_federation_council_id: str
    council_family: SuccessorCouncilFamily
    governed_registry_refs: List[str] = Field(default_factory=list)
    participant_refs: List[str] = Field(default_factory=list)
    cases: List[SuccessorFederationCaseRecord] = Field(default_factory=list)
    quorum_policy_ref: str = "strict_quorum"
    convergence_policy_ref: str = "stable_convergence_required"
    health_status: str = "healthy"
    warnings: List[str] = Field(default_factory=list)

class ExceptionLineageEntryRecord(BaseModel):
    lineage_entry_id: str
    exception_ref: str
    parent_exception_refs: List[str] = Field(default_factory=list)
    child_exception_refs: List[str] = Field(default_factory=list)
    source_decision_refs: List[str] = Field(default_factory=list)
    successor_dependency_refs: List[str] = Field(default_factory=list)
    currentness_state: str = "current"
    expiry_state: str = "valid"
    status: ExceptionLineageEntryStatus = ExceptionLineageEntryStatus.lineage_current
    warnings: List[str] = Field(default_factory=list)

class ExceptionLineageChainRecord(BaseModel):
    chain_id: str
    origin_exception_ref: str
    derived_exception_refs: List[str] = Field(default_factory=list)
    replay_events: List[str] = Field(default_factory=list)
    expiry_transitions: List[str] = Field(default_factory=list)
    is_fragmented: bool = False

class ExceptionLineageRegistryRecord(BaseModel):
    exception_lineage_registry_id: str
    registry_family: ExceptionLineageRegistryFamily
    entries: List[ExceptionLineageEntryRecord] = Field(default_factory=list)
    chains: List[ExceptionLineageChainRecord] = Field(default_factory=list)
    health_status: str = "healthy"
    warnings: List[str] = Field(default_factory=list)

class StabilizationProgramCheckpointRecord(BaseModel):
    checkpoint_id: str
    family: StabilizationCheckpointFamily
    is_cleared: bool = False
    evidence_refs: List[str] = Field(default_factory=list)

class StabilizationProgramStageRecord(BaseModel):
    stage_id: str
    stage_family: StabilizationStage
    entry_conditions: List[str] = Field(default_factory=list)
    exit_conditions: List[str] = Field(default_factory=list)
    downgrade_rules: List[str] = Field(default_factory=list)
    recovery_bias: str = "neutral"

class SovereignGovernanceStabilizationProgramRecord(BaseModel):
    stabilization_program_id: str
    program_family: StabilizationProgramFamily
    monitored_scope_refs: List[str] = Field(default_factory=list)
    stages: List[StabilizationProgramStageRecord] = Field(default_factory=list)
    checkpoints: List[StabilizationProgramCheckpointRecord] = Field(default_factory=list)
    current_stage: StabilizationStage = StabilizationStage.monitoring
    decision: Optional[StabilizationDecision] = None
    warnings: List[str] = Field(default_factory=list)

class GovernanceStabilizationManifestRecord(BaseModel):
    timestamp: str
    recovery_meshes: List[RecoveryQuorumMeshRecord]
    successor_councils: List[SuccessorFederationCouncilRecord]
    lineage_registries: List[ExceptionLineageRegistryRecord]
    stabilization_programs: List[SovereignGovernanceStabilizationProgramRecord]
    system_health: str
