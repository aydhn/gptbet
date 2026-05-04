from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

# Quorum Attestation Exchange Contracts

class QuorumExchangeScopeRecord(BaseModel):
    allowed_domains: List[str]
    time_window_seconds: int

class QuorumExchangeConstraintRecord(BaseModel):
    max_caveat_count: int
    require_fresh_evidence: bool

class QuorumExchangeManifestRecord(BaseModel):
    manifest_id: str
    generated_at: datetime
    exchange_count: int
    warning_count: int

class QuorumExchangeWarningRecord(BaseModel):
    warning_code: str
    description: str
    severity: str

class QuorumExchangeVerificationRecord(BaseModel):
    verification_id: str
    verified_at: datetime
    is_valid: bool

class QuorumExchangeReplayRecord(BaseModel):
    replay_id: str
    replayed_at: datetime
    match_status: str

class QuorumExchangeProjectionRecord(BaseModel):
    projection_id: str
    projected_state: str

class QuorumExchangeHealthRecord(BaseModel):
    health_status: str
    last_check_at: datetime

class QuorumAttestationExchangeRecord(BaseModel):
    quorum_exchange_id: str
    source_attestation_refs: List[str]
    source_council_refs: List[str]
    target_scope_refs: List[str]
    exchange_scope: QuorumExchangeScopeRecord
    preserved_caveat_refs: List[str]
    currentness_refs: List[str]
    validity_window: int
    replay_support_refs: List[str]
    exchange_status: str
    warnings: List[QuorumExchangeWarningRecord] = Field(default_factory=list)

class QuorumExchangePacketRecord(BaseModel):
    quorum_exchange_packet_id: str
    source_attestation_ref: str
    source_decision_lineage_refs: List[str]
    attested_decision_type: str
    preserved_vote_refs: List[str]
    preserved_evidence_refs: List[str]
    caveat_refs: List[str]
    currentness_refs: List[str]
    scope_constraints: QuorumExchangeConstraintRecord
    warnings: List[QuorumExchangeWarningRecord] = Field(default_factory=list)

class QuorumExchangeEnvelopeRecord(BaseModel):
    envelope_id: str
    packets: List[QuorumExchangePacketRecord]
    created_at: datetime

# Backplane Cluster Orchestration Contracts

class BackplaneClusterChannelRecord(BaseModel):
    channel_id: str
    channel_type: str

class BackplaneClusterSegmentRecord(BaseModel):
    segment_id: str
    capacity_weight: float

class BackplaneClusterScheduleRecord(BaseModel):
    schedule_id: str
    active_window: str

class BackplaneClusterCapacityRecord(BaseModel):
    max_ingress_rate: float
    max_replay_load: float

class BackplaneClusterBackpressureRecord(BaseModel):
    pressure_level: str
    affected_channels: List[str]

class BackplaneClusterFailoverRecord(BaseModel):
    failover_target_id: str
    activation_threshold: float

class BackplaneClusterHealthRecord(BaseModel):
    status: str
    last_checked: datetime

class BackplaneClusterManifestRecord(BaseModel):
    manifest_id: str
    cluster_count: int

class BackplaneClusterWarningRecord(BaseModel):
    warning_code: str
    description: str

class BackplaneClusterRecord(BaseModel):
    backplane_cluster_id: str
    cluster_family: str
    node_refs: List[str]
    segment_refs: List[str]
    channel_refs: List[str]
    capacity_refs: List[str]
    orchestration_policy_ref: str
    failover_policy_ref: str
    health_status: str
    warnings: List[BackplaneClusterWarningRecord] = Field(default_factory=list)

class BackplaneClusterNodeRecord(BaseModel):
    node_id: str
    node_family: str
    hosted_segment_refs: List[str]
    hosted_channel_refs: List[str]
    pressure_state: str
    freshness_state: str
    replay_load: float
    node_status: str
    warnings: List[BackplaneClusterWarningRecord] = Field(default_factory=list)

class BackplaneClusterMembershipRecord(BaseModel):
    membership_id: str
    cluster_ref: str
    node_ref: str
    joined_at: datetime

# Baseline Mesh Council Contracts

class BaselineCouncilInputRecord(BaseModel):
    input_id: str
    data_ref: str

class BaselineCouncilEvidenceRecord(BaseModel):
    evidence_id: str
    confidence_score: float

class BaselineCouncilDecisionRecord(BaseModel):
    decision_id: str
    outcome: str

class BaselineCouncilQuorumRecord(BaseModel):
    quorum_id: str
    required_votes: int
    current_votes: int

class BaselineCouncilApplicabilityRecord(BaseModel):
    applicability_id: str
    is_applicable: bool

class BaselineCouncilSupersessionRecord(BaseModel):
    supersession_id: str
    superseded_by_ref: str

class BaselineCouncilHealthRecord(BaseModel):
    health_status: str
    last_checked: datetime

class BaselineMeshCouncilManifestRecord(BaseModel):
    manifest_id: str
    council_count: int

class BaselineMeshCouncilWarningRecord(BaseModel):
    warning_code: str
    description: str

class BaselineMeshCouncilRecord(BaseModel):
    baseline_council_id: str
    council_family: str
    governed_mesh_refs: List[str]
    participant_refs: List[str]
    quorum_policy_ref: str
    precedence_policy_ref: str
    health_status: str
    warnings: List[BaselineMeshCouncilWarningRecord] = Field(default_factory=list)

class BaselineCouncilCaseRecord(BaseModel):
    baseline_case_id: str
    case_family: str
    source_baseline_refs: List[str]
    conflicting_baseline_refs: List[str]
    currentness_projection_refs: List[str]
    applicability_refs: List[str]
    successor_refs: List[str]
    replay_requirement: str
    case_status: str
    warnings: List[BaselineMeshCouncilWarningRecord] = Field(default_factory=list)


# Sovereign Governance Exception Ledger Contracts

class ExceptionScopeRecord(BaseModel):
    affected_domains: List[str]

class ExceptionConstraintRecord(BaseModel):
    max_duration_seconds: int

class ExceptionValidityRecord(BaseModel):
    is_valid: bool
    checked_at: datetime

class ExceptionEvidenceRecord(BaseModel):
    evidence_id: str
    description: str

class ExceptionReplayRecord(BaseModel):
    replay_id: str
    status: str

class ExceptionDecisionRecord(BaseModel):
    decision_id: str
    outcome: str

class ExceptionExpiryRecord(BaseModel):
    expires_at: datetime
    is_expired: bool

class ExceptionSupersessionRecord(BaseModel):
    superseded_by: str

class ExceptionHealthRecord(BaseModel):
    status: str
    last_checked: datetime

class ExceptionLedgerManifestRecord(BaseModel):
    manifest_id: str
    entry_count: int

class ExceptionLedgerWarningRecord(BaseModel):
    warning_code: str
    description: str

class SovereignGovernanceExceptionLedgerRecord(BaseModel):
    exception_ledger_id: str
    ledger_family: str
    owning_scope_ref: str
    active_exception_refs: List[str]
    expired_exception_refs: List[str]
    superseded_exception_refs: List[str]
    replay_refs: List[str]
    health_status: str
    warnings: List[ExceptionLedgerWarningRecord] = Field(default_factory=list)

class GovernanceExceptionRecord(BaseModel):
    exception_id: str
    exception_family: str
    opened_reason: str
    affected_scope_ref: str
    bounded_effect_summary: str
    preserved_block_refs: List[str]
    preserved_caveat_refs: List[str]
    validity_window: int
    evidence_refs: List[str]
    decision_status: str
    warnings: List[ExceptionLedgerWarningRecord] = Field(default_factory=list)
