from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field

# Core Enums
class SignerTrustLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL_AUTHORITY = "critical_authority"

class SignerStatus(str, Enum):
    ACTIVE = "active"
    PROBATION = "probation"
    SUSPENDED = "suspended"
    REVOKED = "revoked"

class AttestationType(str, Enum):
    PROVENANCE = "provenance_attestation"
    REVIEW = "review_attestation"
    ENVIRONMENT = "environment_attestation"
    DISTRIBUTION = "distribution_attestation"
    INTEGRITY = "integrity_attestation"
    SIGNER_SCOPE = "signer_scope_attestation"

class AttestationStatus(str, Enum):
    VALID_SUPPORTING = "valid_supporting"
    VALID_NONBINDING = "valid_but_nonbinding"
    STALE = "stale_attestation"
    SCOPE_MISMATCH = "scope_mismatch"
    UNVERIFIABLE = "unverifiable"
    INVALID = "invalid_attestation"
    PROVIDER_UNTRUSTED = "attestation_provider_untrusted"

class ApprovalStatus(str, Enum):
    CREATED = "approval_created"
    COLLECTING = "collecting_signatures"
    QUORUM_CANDIDATE = "quorum_candidate"
    THRESHOLD_SATISFIED = "threshold_satisfied"
    THRESHOLD_FAILED = "threshold_failed"
    PENDING_ATTESTATION = "pending_attestation"
    FULLY_VERIFIED = "fully_verified"
    REJECTED = "rejected"
    EXPIRED = "expired"
    SUPERSEDED = "superseded"
    REVOKED = "revoked_after_approval"

class TrustMode(str, Enum):
    STRICT_ACTIVE = "strict_active_trust_mode"
    BALANCED_REVIEW = "balanced_review_trust_mode"
    EMERGENCY_STRICT = "emergency_strict_mode"
    IMPORT_QUARANTINE = "import_quarantine_trust_mode"
    DEV_WARN_ONLY = "dev_warn_only_trust_mode"

class ImportLane(str, Enum):
    LOCAL_VERIFIED = "local_verified_candidate"
    FEDERATED_VERIFIED = "federated_verified_candidate"
    REVIEW_QUARANTINE = "review_quarantine"
    TRUST_PENDING = "trust_pending"
    REJECTED_UNTRUSTED = "rejected_untrusted"
    REJECTED_INCOMPATIBLE = "rejected_incompatible"
    EMERGENCY_ONLY = "emergency_only_bundle"
    SHADOW_ONLY = "shadow_policy_only"


# Signer and Group Models
class SignerGroupCapabilityRecord(BaseModel):
    group_name: str
    allowed_target_families: List[str]
    is_active_signing: bool = True
    veto_capability: bool = False

class SignerGroupTrustPolicyRecord(BaseModel):
    group_name: str
    base_weight: float
    max_weight_cap: float

class SignerGroupRecord(BaseModel):
    group_name: str
    capabilities: SignerGroupCapabilityRecord
    trust_policy: SignerGroupTrustPolicyRecord
    quorum_contribution_value: float = 1.0

class SignerMembershipRecord(BaseModel):
    signer_id: str
    group_names: List[str]
    roles: List[str] = Field(default_factory=list)

class ApprovalSignerRecord(BaseModel):
    signer_id: str
    trust_level: SignerTrustLevel
    status: SignerStatus
    membership: SignerMembershipRecord
    base_weight_override: Optional[float] = None


# Threshold & Policy Models
class MandatoryPresenceRuleRecord(BaseModel):
    required_group: str
    min_count: int = 1

class VetoRuleRecord(BaseModel):
    veto_enabled_groups: List[str]
    requires_explanation: bool = True

class ApprovalThresholdPolicyRecord(BaseModel):
    threshold_policy_id: str
    policy_family: str
    target_scope: Dict[str, Any]
    min_signer_count: int
    min_weighted_trust: float
    mandatory_signer_groups: List[MandatoryPresenceRuleRecord] = Field(default_factory=list)
    disallowed_signer_groups: List[str] = Field(default_factory=list)
    veto_rules: Optional[VetoRuleRecord] = None
    attestation_requirements: List[str] = Field(default_factory=list)
    expiry_seconds: int = 86400
    warnings: List[str] = Field(default_factory=list)

class SignerQuorumSetRecord(BaseModel):
    quorum_id: str
    required_policies: List[ApprovalThresholdPolicyRecord]


# Approval & Evaluation Models
class MultiSignerWarningRecord(BaseModel):
    warning_code: str
    message: str

class VetoDecisionRecord(BaseModel):
    signer_id: str
    group_name: str
    reason: str
    timestamp: datetime

class WeightedTrustRecord(BaseModel):
    signer_id: str
    computed_weight: float
    modifiers_applied: List[str]
    is_capped: bool

class QuorumEvaluationRecord(BaseModel):
    evaluation_id: str
    policy_ref: str
    signer_count_satisfied: bool
    weighted_trust_satisfied: bool
    mandatory_presence_satisfied: bool
    vetoes_present: bool
    total_signers: int
    total_weighted_trust: float
    veto_records: List[VetoDecisionRecord] = Field(default_factory=list)

class MultiSignerApprovalRecord(BaseModel):
    multi_approval_id: str
    target_family: str
    target_ref: str
    approval_policy_ref: str
    required_quorum: SignerQuorumSetRecord
    collected_signatures: List[str]  # signer ids
    weighted_trust_total: float = 0.0
    current_status: ApprovalStatus = ApprovalStatus.CREATED
    approval_deadline: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    warnings: List[MultiSignerWarningRecord] = Field(default_factory=list)


# Attestation Models
class AttestationProviderRecord(BaseModel):
    provider_id: str
    provider_type: str
    trust_weight_boost_cap: float = 0.0

class AttestationScopeRecord(BaseModel):
    target_family: str
    target_refs: List[str]

class AttestationEvidenceRecord(BaseModel):
    evidence_id: str
    payload_hash: str
    signature: str

class AttestationTrustEffectRecord(BaseModel):
    applied_boost: float
    conditions: List[str]

class AttestationStatementRecord(BaseModel):
    statement_id: str
    provider_id: str
    attestation_type: AttestationType
    scope: AttestationScopeRecord
    evidence: AttestationEvidenceRecord
    issued_at: datetime
    expires_at: Optional[datetime] = None

class AttestationVerificationRecord(BaseModel):
    verification_id: str
    statement_ref: str
    status: AttestationStatus
    trust_effect: Optional[AttestationTrustEffectRecord] = None
    verified_at: datetime

class AttestationRecord(BaseModel):
    attestation_id: str
    statement: AttestationStatementRecord
    verification: Optional[AttestationVerificationRecord] = None


# Federated Verification Mesh Models
class TrustMeshNodeRecord(BaseModel):
    node_id: str
    plane_type: str
    trust_level: str

class TrustMeshEdgeRecord(BaseModel):
    source_node: str
    target_node: str
    relationship: str

class DistributionMeshRecord(BaseModel):
    mesh_id: str
    nodes: List[TrustMeshNodeRecord]
    edges: List[TrustMeshEdgeRecord]

class MeshVerificationRequestRecord(BaseModel):
    request_id: str
    target_bundle_ref: str
    source_node: str
    requested_at: datetime

class MeshVerificationResponseRecord(BaseModel):
    response_id: str
    request_ref: str
    responder_node: str
    is_verified: bool
    signatures_provided: List[str]
    responded_at: datetime

class FederatedVerificationRecord(BaseModel):
    verification_id: str
    bundle_ref: str
    local_verified: bool
    remote_responses: List[MeshVerificationResponseRecord]
    final_lane: ImportLane

class FederatedImportDecisionRecord(BaseModel):
    decision_id: str
    verification_ref: str
    accepted: bool
    lane_assigned: ImportLane
    reason: str

class CrossPlaneVerificationProofRecord(BaseModel):
    proof_id: str
    federated_decision_ref: str
    signatures: List[str]


# Chain and Proof Models
class ApprovalChainLinkRecord(BaseModel):
    link_id: str
    previous_link_id: Optional[str]
    action_type: str
    actor: str
    timestamp: datetime
    payload_hash: str

class ApprovalChainHashRecord(BaseModel):
    chain_id: str
    root_hash: str
    head_hash: str
    link_count: int

class ApprovalChainSummaryRecord(BaseModel):
    chain_id: str
    status: str
    start_time: datetime
    end_time: Optional[datetime]

class ApprovalProofChainRecord(BaseModel):
    chain_id: str
    links: List[ApprovalChainLinkRecord]
    summary: ApprovalChainSummaryRecord
    hash_record: ApprovalChainHashRecord

class ThresholdDecisionRecord(BaseModel):
    decision_id: str
    target_ref: str
    approval_ref: str
    quorum_ref: str
    attestation_refs: List[str]
    is_approved: bool
    proof_chain_ref: str
    ledger_ref: Optional[str] = None
    created_at: datetime


# Emergency & Break Glass Models
class EmergencySignerConstraintRecord(BaseModel):
    required_groups: List[str]
    min_weight: float

class EmergencyApprovalWindowRecord(BaseModel):
    max_duration_seconds: int
    requires_post_review: bool

class EmergencyTrustPolicyRecord(BaseModel):
    emergency_policy_id: str
    base_policy_ref: str
    signer_constraints: EmergencySignerConstraintRecord
    window: EmergencyApprovalWindowRecord

class BreakGlassReviewRequirementRecord(BaseModel):
    required_reviewer_groups: List[str]
    deadline_seconds: int

class BreakGlassExpiryRecord(BaseModel):
    expires_at: datetime
    action_on_expiry: str

class BreakGlassJustificationRecord(BaseModel):
    reason: str
    incident_ref: Optional[str]
    declared_by: str

class BreakGlassRecord(BaseModel):
    break_glass_id: str
    target_ref: str
    justification: BreakGlassJustificationRecord
    expiry: BreakGlassExpiryRecord
    review_requirement: BreakGlassReviewRequirementRecord
    is_active: bool
    created_at: datetime

class TrustExceptionRecord(BaseModel):
    exception_id: str
    exception_type: str
    details: Dict[str, Any]


# High Level Manifest & Audit
class MultiSignerAuditRecord(BaseModel):
    audit_id: str
    target_ref: str
    action: str
    status: str
    timestamp: datetime

class TrustGovernanceManifest(BaseModel):
    manifest_id: str
    version: str
    active_policies: List[str]
    active_signers: int
    recent_decisions: int
    generated_at: datetime
    mode: TrustMode
