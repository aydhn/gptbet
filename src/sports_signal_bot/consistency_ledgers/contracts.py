from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# TAXONOMIES
# ---------------------------------------------------------------------------


class AlignmentFederationFamily(str, Enum):
    CONTEXT_ALIGNMENT_FEDERATION = "context_alignment_federation"
    TRACE_AND_PROOF_ALIGNMENT_FEDERATION = "trace_and_proof_alignment_federation"
    FRESHNESS_ALIGNMENT_FEDERATION = "freshness_alignment_federation"
    EXCHANGE_INTEGRITY_ALIGNMENT_FEDERATION = "exchange_integrity_alignment_federation"
    SOVEREIGNTY_PRESERVATION_ALIGNMENT_FEDERATION = (
        "sovereignty_preservation_alignment_federation"
    )
    NO_SAFE_VISIBILITY_ALIGNMENT_FEDERATION = "no_safe_visibility_alignment_federation"
    COMPOSITE_GOVERNANCE_ALIGNMENT_FEDERATION = (
        "composite_governance_alignment_federation"
    )


class FederationLinkStatus(str, Enum):
    LINK_CURRENT = "link_current"
    LINK_CAVEATED = "link_caveated"
    LINK_REVIEW_ONLY = "link_review_only"
    LINK_DEGRADED = "link_degraded"
    LINK_BLOCKED = "link_blocked"
    LINK_EXPIRED = "link_expired"
    LINK_SUPERSEDED = "link_superseded"


class FederatedAlignmentOutputStatus(str, Enum):
    FEDERATED_ALIGNMENT_CURRENT_WITH_CAPS = "federated_alignment_current_with_caps"
    FEDERATED_ALIGNMENT_CAVEATED = "federated_alignment_caveated"
    FEDERATED_ALIGNMENT_REVIEW_ONLY = "federated_alignment_review_only"
    FEDERATED_ALIGNMENT_DEGRADED = "federated_alignment_degraded"
    FEDERATED_ALIGNMENT_BLOCKED = "federated_alignment_blocked"
    FEDERATED_ALIGNMENT_STALE = "federated_alignment_stale"


class AlignmentAgreementBand(str, Enum):
    NO_AGREEMENT = "no_agreement"
    WEAK_AGREEMENT = "weak_agreement"
    BOUNDED_AGREEMENT = "bounded_agreement"
    STRONG_AGREEMENT_WITH_CAVEATS = "strong_agreement_with_caveats"
    STABLE_AGREEMENT = "stable_agreement"


class TribunalMeshFamily(str, Enum):
    BOUNDED_CONTEXT_DISPUTE_MESH = "bounded_context_dispute_mesh"
    FRESHNESS_CONFLICT_MESH = "freshness_conflict_mesh"
    TRACE_CONTEXT_CONFLICT_MESH = "trace_context_conflict_mesh"
    SOVEREIGNTY_VISIBILITY_MESH = "sovereignty_visibility_mesh"
    NO_SAFE_VISIBILITY_MESH = "no_safe_visibility_mesh"
    DEGRADED_DISPUTE_MESH = "degraded_dispute_mesh"
    COMPOSITE_TRIBUNAL_MESH = "composite_tribunal_mesh"


class TribunalNodeFamily(str, Enum):
    TRIBUNAL_INGRESS_NODE = "tribunal_ingress_node"
    FRESHNESS_REVIEW_NODE = "freshness_review_node"
    TRACE_INTEGRITY_NODE = "trace_integrity_node"
    PROOF_SUFFICIENCY_NODE = "proof_sufficiency_node"
    SOVEREIGNTY_GUARD_NODE = "sovereignty_guard_node"
    NO_SAFE_VISIBILITY_NODE = "no_safe_visibility_node"
    DEGRADED_FALLBACK_NODE = "degraded_fallback_node"
    MESH_HEALTH_OBSERVER_NODE = "mesh_health_observer_node"


class TribunalMeshEdgeStatus(str, Enum):
    EDGE_CURRENT = "edge_current"
    EDGE_CAVEATED = "edge_caveated"
    EDGE_REVIEW_ONLY = "edge_review_only"
    EDGE_DEGRADED = "edge_degraded"
    EDGE_BACKPRESSURED = "edge_backpressured"
    EDGE_BLOCKED = "edge_blocked"
    EDGE_EXPIRED = "edge_expired"
    EDGE_SUPERSEDED = "edge_superseded"


class TribunalMeshRouteOutcome(str, Enum):
    BOUNDED_TRIBUNAL_ROUTE = "bounded_tribunal_route"
    REVIEW_ONLY_TRIBUNAL_ROUTE = "review_only_tribunal_route"
    CAVEATED_TRIBUNAL_ROUTE = "caveated_tribunal_route"
    DEGRADED_TRIBUNAL_ROUTE = "degraded_tribunal_route"
    REPLAY_REQUIRED_TRIBUNAL_ROUTE = "replay_required_tribunal_route"
    BLOCKED_TRIBUNAL_ROUTE = "blocked_tribunal_route"
    NO_SAFE_TRIBUNAL_ROUTE = "no_safe_tribunal_route"


class MeshPressureState(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"
    SUPPRESS_NONCRITICAL_TRIBUNAL_PATHS = "suppress_noncritical_tribunal_paths"
    REVIEW_ONLY_BIAS = "review_only_bias"


class EvidenceClearerFamily(str, Enum):
    BOUNDED_EVIDENCE_CLEARER = "bounded_evidence_clearer"
    REVIEW_ONLY_EVIDENCE_CLEARER = "review_only_evidence_clearer"
    PROOF_SUPPORT_EVIDENCE_CLEARER = "proof_support_evidence_clearer"
    CONTEXT_SUPPORT_EVIDENCE_CLEARER = "context_support_evidence_clearer"
    DEGRADED_EVIDENCE_CLEARER = "degraded_evidence_clearer"
    SOVEREIGNTY_WARNING_EVIDENCE_CLEARER = "sovereignty_warning_evidence_clearer"
    COMPOSITE_EVIDENCE_CLEARER = "composite_evidence_clearer"


class ClearingStatus(str, Enum):
    CLEARING_READY = "clearing_ready"
    CLEARING_CAVEATED = "clearing_caveated"
    CLEARING_REVIEW_ONLY = "clearing_review_only"
    CLEARING_BACKPRESSURED = "clearing_backpressured"
    CLEARING_DEGRADED = "clearing_degraded"
    CLEARING_BLOCKED = "clearing_blocked"
    CLEARING_SUPERSEDED = "clearing_superseded"


class ClearingOutcome(str, Enum):
    CLEARED_BOUNDED_EVIDENCE_ROUTE = "cleared_bounded_evidence_route"
    CLEARED_REVIEW_ONLY_EVIDENCE_ROUTE = "cleared_review_only_evidence_route"
    CLEARED_CAVEATED_EVIDENCE_ROUTE = "cleared_caveated_evidence_route"
    CLEARED_DEGRADED_EVIDENCE_ROUTE = "cleared_degraded_evidence_route"
    CLEARING_REVALIDATION_REQUIRED = "clearing_revalidation_required"
    CLEARING_BLOCKED = "clearing_blocked"
    NO_SAFE_CLEARING_ROUTE = "no_safe_clearing_route"


class ConsistencyLedgerFamily(str, Enum):
    GOVERNANCE_CONSISTENCY_LEDGER = "governance_consistency_ledger"
    FRESHNESS_CONSISTENCY_LEDGER = "freshness_consistency_ledger"
    TRACE_CONSISTENCY_LEDGER = "trace_consistency_ledger"
    EXCHANGE_CONSISTENCY_LEDGER = "exchange_consistency_ledger"
    SOVEREIGNTY_CONSISTENCY_LEDGER = "sovereignty_consistency_ledger"
    NO_SAFE_VISIBILITY_CONSISTENCY_LEDGER = "no_safe_visibility_consistency_ledger"
    COMPOSITE_CONSISTENCY_LEDGER = "composite_consistency_ledger"


class LedgerEntryFamily(str, Enum):
    CONTEXT_CONSISTENCY_ENTRY = "context_consistency_entry"
    PROOF_FRESHNESS_CONSISTENCY_ENTRY = "proof_freshness_consistency_entry"
    TRACE_INTEGRITY_CONSISTENCY_ENTRY = "trace_integrity_consistency_entry"
    EXCHANGE_INTEGRITY_CONSISTENCY_ENTRY = "exchange_integrity_consistency_entry"
    SOVEREIGNTY_VISIBILITY_CONSISTENCY_ENTRY = (
        "sovereignty_visibility_consistency_entry"
    )
    NO_SAFE_VISIBILITY_CONSISTENCY_ENTRY = "no_safe_visibility_consistency_entry"
    BURDEN_VISIBILITY_CONSISTENCY_ENTRY = "burden_visibility_consistency_entry"
    CONTRADICTION_ENTRY = "contradiction_entry"


class ConsistencyState(str, Enum):
    CONSISTENT_WITH_CAPS = "consistent_with_caps"
    CAVEATED_CONSISTENCY = "caveated_consistency"
    REVIEW_ONLY_CONSISTENCY = "review_only_consistency"
    DEGRADED_CONSISTENCY = "degraded_consistency"
    CONTRADICTED = "contradicted"
    STALE_CONSISTENCY = "stale_consistency"
    BLOCKED_CONSISTENCY = "blocked_consistency"


class ContradictionFamily(str, Enum):
    FRESHNESS_CONTRADICTION = "freshness_contradiction"
    TRACE_CONTRADICTION = "trace_contradiction"
    PROOF_CONTEXT_CONTRADICTION = "proof_context_contradiction"
    EXCHANGE_CAVEAT_CONTRADICTION = "exchange_caveat_contradiction"
    SOVEREIGNTY_VISIBILITY_CONTRADICTION = "sovereignty_visibility_contradiction"
    NO_SAFE_VISIBILITY_CONTRADICTION = "no_safe_visibility_contradiction"
    AUDIENCE_SCOPE_CONTRADICTION = "audience_scope_contradiction"
    BURDEN_OBSCURATION_CONTRADICTION = "burden_obscuration_contradiction"


class ConsistencyShiftFamily(str, Enum):
    IMPROVED_CONSISTENCY = "improved_consistency"
    STABLE_CONSISTENCY = "stable_consistency"
    DEGRADED_CONSISTENCY = "degraded_consistency"
    NEWLY_CONTRADICTED = "newly_contradicted"
    CONTRADICTION_RESOLVED = "contradiction_resolved"
    REPLAY_REVALIDATED = "replay_revalidated"
    CEILING_LOWERED = "ceiling_lowered"
    NO_SAFE_VISIBILITY_RESTORED = "no_safe_visibility_restored"


class HealthStatus(str, Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    CRITICAL = "critical"


# ---------------------------------------------------------------------------
# DATA STRUCTURES
# ---------------------------------------------------------------------------


class AlignmentCompilerFederationRecord(BaseModel):
    alignment_federation_id: str
    federation_family: AlignmentFederationFamily
    member_alignment_compiler_refs: List[str]
    active_link_refs: List[str]
    currentness_policy_ref: str
    ceiling_policy_ref: str
    agreement_policy_ref: str
    health_status: HealthStatus = HealthStatus.HEALTHY
    warnings: List[str] = Field(default_factory=list)


class FederatedAlignmentNodeRecord(BaseModel):
    node_id: str
    alignment_compiler_ref: str
    compiler_family: str
    supported_scope_refs: List[str]
    currentness_state: str
    penalty_state: str
    sovereignty_state: str
    node_status: str
    warnings: List[str] = Field(default_factory=list)


class AlignmentFederationLinkRecord(BaseModel):
    link_id: str
    source_node_ref: str
    target_node_ref: str
    link_status: FederationLinkStatus
    warnings: List[str] = Field(default_factory=list)


class AlignmentFederationCurrentnessRecord(BaseModel):
    record_id: str
    federation_id: str
    is_current: bool
    stale_node_refs: List[str]
    warnings: List[str] = Field(default_factory=list)


class AlignmentFederationPenaltyRecord(BaseModel):
    record_id: str
    federation_id: str
    penalties: List[str]
    warnings: List[str] = Field(default_factory=list)


class AlignmentFederationCeilingRecord(BaseModel):
    record_id: str
    federation_id: str
    ceilings: List[str]
    warnings: List[str] = Field(default_factory=list)


class AlignmentFederationAgreementRecord(BaseModel):
    record_id: str
    federation_id: str
    agreement_band: AlignmentAgreementBand
    warnings: List[str] = Field(default_factory=list)


class AlignmentFederationDecisionRecord(BaseModel):
    record_id: str
    federation_id: str
    decision_output: FederatedAlignmentOutputStatus
    warnings: List[str] = Field(default_factory=list)


class AlignmentFederationHealthRecord(BaseModel):
    record_id: str
    federation_id: str
    health_status: HealthStatus
    warnings: List[str] = Field(default_factory=list)


class AlignmentCompilerFederationManifestRecord(BaseModel):
    manifest_id: str
    federation_records: List[AlignmentCompilerFederationRecord]
    warnings: List[str] = Field(default_factory=list)


class AlignmentCompilerFederationWarningRecord(BaseModel):
    warning_id: str
    federation_id: str
    message: str


class DisputeTribunalMeshRecord(BaseModel):
    tribunal_mesh_id: str
    mesh_family: TribunalMeshFamily
    node_refs: List[str]
    edge_refs: List[str]
    case_refs: List[str]
    routing_policy_ref: str
    escalation_policy_ref: str
    pressure_policy_ref: str
    health_status: HealthStatus = HealthStatus.HEALTHY
    warnings: List[str] = Field(default_factory=list)


class TribunalMeshNodeRecord(BaseModel):
    node_id: str
    node_family: TribunalNodeFamily
    hosted_tribunal_refs: List[str]
    supported_case_families: List[str]
    currentness_state: str
    backlog_state: str
    node_status: str
    warnings: List[str] = Field(default_factory=list)


class TribunalMeshEdgeRecord(BaseModel):
    edge_id: str
    source_node_ref: str
    target_node_ref: str
    supported_case_families: List[str]
    supported_scope_classes: List[str]
    caveat_transfer_policy: str
    currentness_state: str
    edge_status: TribunalMeshEdgeStatus
    warnings: List[str] = Field(default_factory=list)


class TribunalMeshPathRecord(BaseModel):
    path_id: str
    mesh_id: str
    edge_sequence: List[str]
    outcome: TribunalMeshRouteOutcome
    warnings: List[str] = Field(default_factory=list)


class TribunalMeshCaseRecord(BaseModel):
    case_id: str
    mesh_id: str
    status: str
    warnings: List[str] = Field(default_factory=list)


class TribunalMeshConstraintRecord(BaseModel):
    constraint_id: str
    mesh_id: str
    rules: Dict[str, Any]


class TribunalMeshDecisionRecord(BaseModel):
    decision_id: str
    case_id: str
    outcome: str


class TribunalMeshPressureRecord(BaseModel):
    record_id: str
    mesh_id: str
    pressure_state: MeshPressureState
    metrics: Dict[str, float]
    warnings: List[str] = Field(default_factory=list)


class TribunalMeshHealthRecord(BaseModel):
    record_id: str
    mesh_id: str
    health_status: HealthStatus
    warnings: List[str] = Field(default_factory=list)


class DisputeTribunalMeshManifestRecord(BaseModel):
    manifest_id: str
    mesh_records: List[DisputeTribunalMeshRecord]


class DisputeTribunalMeshWarningRecord(BaseModel):
    warning_id: str
    mesh_id: str
    message: str


class EvidenceExchangeClearerRecord(BaseModel):
    evidence_clearer_id: str
    clearer_family: EvidenceClearerFamily
    source_exchange_refs: List[str]
    clearing_book_refs: List[str]
    active_listing_refs: List[str]
    active_request_refs: List[str]
    active_match_refs: List[str]
    fairness_policy_ref: str
    health_status: HealthStatus = HealthStatus.HEALTHY
    warnings: List[str] = Field(default_factory=list)


class ClearingBookRecord(BaseModel):
    clearing_book_id: str
    exchange_family: str
    scope_class: str
    compatible_listing_refs: List[str]
    compatible_request_refs: List[str]
    backlog_refs: List[str]
    pressure_state: str
    clearing_status: ClearingStatus
    warnings: List[str] = Field(default_factory=list)


class ClearingListingRecord(BaseModel):
    listing_id: str
    listing_family: str
    source_ref: str
    source_family: str
    supported_trace_families: List[str]
    supported_audience_profiles: List[str]
    evidence_completeness: float
    currentness_state: str
    caveat_refs: List[str]
    listing_status: str
    warnings: List[str] = Field(default_factory=list)


class ClearingRequestRecord(BaseModel):
    request_id: str
    target_context_ref: str
    requested_trace_family: str
    required_evidence_refs: List[str]
    required_scope_class: str
    required_audience_profile: str
    request_priority: str
    request_status: str
    warnings: List[str] = Field(default_factory=list)


class ClearingMatchRecord(BaseModel):
    match_id: str
    listing_ref: str
    request_ref: str
    outcome: ClearingOutcome
    warnings: List[str] = Field(default_factory=list)


class ClearingConstraintRecord(BaseModel):
    constraint_id: str
    rules: Dict[str, Any]


class ClearingDecisionRecord(BaseModel):
    decision_id: str
    match_ref: str
    final_status: str


class ClearingCeilingRecord(BaseModel):
    ceiling_id: str
    match_ref: str
    ceilings: List[str]


class ClearingFairnessRecord(BaseModel):
    record_id: str
    clearer_id: str
    fairness_score: float
    metrics: Dict[str, float]


class ClearingPressureRecord(BaseModel):
    record_id: str
    clearer_id: str
    pressure_score: float
    metrics: Dict[str, float]


class ClearingHealthRecord(BaseModel):
    record_id: str
    clearer_id: str
    health_status: HealthStatus


class EvidenceExchangeClearerManifestRecord(BaseModel):
    manifest_id: str
    clearer_records: List[EvidenceExchangeClearerRecord]


class EvidenceExchangeClearerWarningRecord(BaseModel):
    warning_id: str
    clearer_id: str
    message: str


class ConsistencyEntryParams(BaseModel):
    family: LedgerEntryFamily
    source_ref: str
    source_family: str
    currentness: str
    consistency: ConsistencyState
    caveats: str


class SovereignGovernanceConsistencyLedgerRecord(BaseModel):
    consistency_ledger_id: str
    ledger_family: ConsistencyLedgerFamily
    entry_refs: List[str]
    contradiction_refs: List[str]
    replay_refs: List[str]
    ceiling_refs: List[str]
    no_safe_refs: List[str]
    health_status: HealthStatus = HealthStatus.HEALTHY
    warnings: List[str] = Field(default_factory=list)


class ConsistencyLedgerEntryRecord(BaseModel):
    consistency_entry_id: str
    entry_family: LedgerEntryFamily
    source_ref: str
    source_family: str
    currentness_state: str
    consistency_state: ConsistencyState
    contradiction_state: str
    caveat_state: str
    warnings: List[str] = Field(default_factory=list)


class ConsistencyOriginRecord(BaseModel):
    origin_id: str
    entry_ref: str
    origin_details: Dict[str, Any]


class ConsistencyShiftRecord(BaseModel):
    shift_id: str
    ledger_id: str
    shift_family: ConsistencyShiftFamily
    previous_state: str
    new_state: str
    reason: str
    warnings: List[str] = Field(default_factory=list)


class ConsistencyContradictionRecord(BaseModel):
    contradiction_id: str
    ledger_id: str
    contradiction_family: ContradictionFamily
    involved_entry_refs: List[str]
    severity: str
    warnings: List[str] = Field(default_factory=list)


class ConsistencyReplayRecord(BaseModel):
    replay_id: str
    ledger_id: str
    status: str


class ConsistencyCeilingRecord(BaseModel):
    ceiling_id: str
    ledger_id: str
    ceilings: List[str]


class ConsistencyNoSafeRecord(BaseModel):
    record_id: str
    ledger_id: str
    no_safe_visibility_retained: bool
    warnings: List[str] = Field(default_factory=list)


class ConsistencyHealthRecord(BaseModel):
    record_id: str
    ledger_id: str
    health_status: HealthStatus
    warnings: List[str] = Field(default_factory=list)


class GovernanceConsistencyLedgerManifestRecord(BaseModel):
    manifest_id: str
    ledger_records: List[SovereignGovernanceConsistencyLedgerRecord]


class GovernanceConsistencyLedgerWarningRecord(BaseModel):
    warning_id: str
    ledger_id: str
    message: str
