from datetime import datetime
from enum import Enum
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class LogFamily(Enum):
    POLICY_TRANSPARENCY_LOG = "policy_transparency_log"
    GOVERNANCE_DECISION_LOG = "governance_decision_log"
    APPROVAL_TRANSPARENCY_LOG = "approval_transparency_log"
    SIGNER_TRUST_LOG = "signer_trust_log"
    OVERRIDE_TRANSPARENCY_LOG = "override_transparency_log"
    ACTIVATION_ROLLBACK_LOG = "activation_rollback_log"
    FEDERATED_IMPORT_LOG = "federated_import_log"
    CROSS_PLANE_EVENT_LOG = "cross_plane_event_log"
    GOVERNANCE_TRANSPARENCY_SUPERLOG = "governance_transparency_superlog"

class EventFamily(Enum):
    SIGNED_POLICY_BUNDLE_PUBLISHED = "signed_policy_bundle_published"
    POLICY_BUNDLE_PROMOTED = "policy_bundle_promoted"
    POLICY_BUNDLE_REVOKED = "policy_bundle_revoked"
    APPLIED_POLICY_SNAPSHOT_CREATED = "applied_policy_snapshot_created"
    CRITICAL_DECISION_PROOF_CREATED = "critical_decision_proof_created"
    MULTI_SIGNER_APPROVAL_FINALIZED = "multi_signer_approval_finalized"
    EMERGENCY_OVERRIDE_ISSUED = "emergency_override_issued"
    EMERGENCY_OVERRIDE_EXPIRED = "emergency_override_expired"
    FAMILY_FREEZE_APPLIED = "family_freeze_applied"
    FAMILY_FREEZE_RELEASED = "family_freeze_released"
    ACTIVATION_APPROVED = "activation_approved"
    ACTIVATION_HELD = "activation_held"
    ACTIVATION_REJECTED = "activation_rejected"
    ROLLBACK_EXECUTED = "rollback_executed"
    SIGNER_TRUST_CHANGED = "signer_trust_changed"
    SIGNER_TRUST_REVOKED = "signer_trust_revoked"
    IMPORTED_BUNDLE_QUARANTINED = "imported_bundle_quarantined"
    IMPORTED_BUNDLE_ACCEPTED = "imported_bundle_accepted"
    FEDERATED_VERIFICATION_COMPLETED = "federated_verification_completed"
    CRITICAL_ESCALATION_RESOLVED = "critical_escalation_resolved"

class InclusionStatus(Enum):
    PENDING = "pending"
    INCLUDED = "included"
    ORPHANED = "orphaned"

class VerificationStatus(Enum):
    UNVERIFIED = "unverified"
    VERIFIED = "verified"
    FAILED = "failed"
    STALE = "stale"
    INCOMPLETE = "incomplete"

class TrustStatus(Enum):
    TRUSTED = "trusted"
    QUARANTINED = "quarantined"
    UNTRUSTED = "untrusted"
    REVIEW_REQUIRED = "review_required"

class TransparencyEntryRecord(BaseModel):
    transparency_entry_id: str
    log_family: LogFamily
    event_family: EventFamily
    event_ref: str
    event_hash: str
    payload_hash: str
    prior_entry_hash: Optional[str] = None
    log_index: int
    inclusion_status: InclusionStatus
    created_at: datetime = Field(default_factory=datetime.utcnow)
    warnings: List[str] = Field(default_factory=list)

class TransparencyCheckpointRecord(BaseModel):
    checkpoint_id: str
    log_id: str
    tree_size: int
    root_hash: str
    prior_checkpoint_ref: Optional[str] = None
    signed_checkpoint_ref: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    warnings: List[str] = Field(default_factory=list)

class CheckpointSignatureRecord(BaseModel):
    signature_id: str
    checkpoint_id: str
    signer_set: List[str]
    threshold_policy_ref: Optional[str] = None
    signature_block: str
    checkpoint_scope: str
    validity_window: Optional[Dict[str, datetime]] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

class CheckpointTrustRecord(BaseModel):
    trust_id: str
    checkpoint_id: str
    trust_status: TrustStatus
    created_at: datetime = Field(default_factory=datetime.utcnow)

class CheckpointVerificationRecord(BaseModel):
    verification_id: str
    checkpoint_id: str
    status: VerificationStatus
    verified_at: datetime = Field(default_factory=datetime.utcnow)

class InclusionProofRecord(BaseModel):
    proof_id: str
    log_id: str
    tree_size: int
    leaf_index: int
    leaf_hash: str
    merkle_path: List[str]
    checkpoint_ref: str
    verification_status: VerificationStatus
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ConsistencyProofRecord(BaseModel):
    proof_id: str
    log_id: str
    old_tree_size: int
    new_tree_size: int
    old_root_hash: str
    new_root_hash: str
    merkle_path: List[str]
    verification_status: VerificationStatus
    created_at: datetime = Field(default_factory=datetime.utcnow)

class MirrorRecord(BaseModel):
    mirror_id: str
    mirror_family: str
    source_log_id: str
    sync_status: str
    latest_seen_checkpoint: Optional[str] = None
    latest_verified_tree_size: int = 0
    trust_status: TrustStatus
    created_at: datetime = Field(default_factory=datetime.utcnow)
    warnings: List[str] = Field(default_factory=list)

class MirrorSyncRecord(BaseModel):
    sync_id: str
    mirror_id: str
    source_checkpoint_ref: str
    status: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class MirrorVerificationRecord(BaseModel):
    verification_id: str
    mirror_id: str
    status: VerificationStatus
    verified_at: datetime = Field(default_factory=datetime.utcnow)

class GossipTopic(Enum):
    POLICY_BUNDLE_UPDATES = "policy_bundle_updates"
    SIGNED_CHECKPOINT_UPDATES = "signed_checkpoint_updates"
    SIGNER_TRUST_UPDATES = "signer_trust_updates"
    EMERGENCY_OVERRIDE_UPDATES = "emergency_override_updates"
    FAMILY_FREEZE_UPDATES = "family_freeze_updates"
    FEDERATED_IMPORT_ALERTS = "federated_import_alerts"
    INTEGRITY_FAILURE_ALERTS = "integrity_failure_alerts"
    ROLLBACK_AND_ACTIVATION_EVENTS = "rollback_and_activation_events"

class GossipSummaryRecord(BaseModel):
    summary_id: str
    topic: GossipTopic
    summary_hash: str
    details: Dict[str, Any]
    created_at: datetime = Field(default_factory=datetime.utcnow)

class GossipEnvelopeRecord(BaseModel):
    envelope_id: str
    source_plane: str
    payload: GossipSummaryRecord
    signature: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class GossipVerificationRecord(BaseModel):
    verification_id: str
    envelope_id: str
    status: VerificationStatus
    verified_at: datetime = Field(default_factory=datetime.utcnow)

class FailureSeverity(Enum):
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class TransparencyFailureRecord(BaseModel):
    failure_id: str
    failure_type: str
    severity: FailureSeverity
    details: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class LedgerTransparencyLinkRecord(BaseModel):
    link_id: str
    ledger_entry_ref: str
    transparency_entry_ref: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class TransparencyLogRecord(BaseModel):
    log_id: str
    family: LogFamily
    entries: List[TransparencyEntryRecord] = Field(default_factory=list)
    checkpoints: List[TransparencyCheckpointRecord] = Field(default_factory=list)

class TrustGossipRecord(BaseModel):
    gossip_id: str
    envelope: GossipEnvelopeRecord
    status: VerificationStatus

class GossipStateHintRecord(BaseModel):
    hint_id: str
    envelope_ref: str
    hint: str

class GossipConflictRecord(BaseModel):
    conflict_id: str
    envelope_ref: str
    conflict_details: str

class GossipFreshnessRecord(BaseModel):
    freshness_id: str
    envelope_ref: str
    freshness_score: float

class TransparencySummaryRecord(BaseModel):
    summary_id: str
    log_families_count: int
    signed_checkpoint_count: int
    inclusion_verification_success_rate: float
    mirror_sync_status_counts: Dict[str, int]
    gossip_verification_matches: int
    gossip_verification_mismatches: int
    transparency_failure_counts: Dict[str, int]
    independently_verified_critical_event_count: int
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ProofTransparencyLinkRecord(BaseModel):
    link_id: str
    decision_proof_ref: str
    transparency_entry_ref: str

class TransparencyChainMapRecord(BaseModel):
    map_id: str
    ledger_entry_hash: str
    transparency_leaf_hash: str

class TransparencyManifest(BaseModel):
    manifest_id: str
    active_logs: List[str]
    active_mirrors: List[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)

class LogRootRecord(BaseModel):
    root_id: str
    log_id: str
    tree_size: int
    root_hash: str

class MerkleLeafRecord(BaseModel):
    leaf_index: int
    leaf_hash: str

class MerklePathRecord(BaseModel):
    path_id: str
    nodes: List[str]

class SignedCheckpointRecord(BaseModel):
    checkpoint_id: str
    signature_block: str
    signer_set: List[str]

class TransparencyWitnessHintRecord(BaseModel):
    hint_id: str
    witness_refs: List[str]

class VerificationMirrorPackageRecord(BaseModel):
    package_id: str
    mirror_id: str
    status: str

class DistributionTransparencyHintRecord(BaseModel):
    hint_id: str
    expected_family: LogFamily
    expected_checkpoint_summary: str

class VerificationHintRecord(BaseModel):
    hint_id: str
    policy: str

class ExpectedCheckpointRecord(BaseModel):
    expected_id: str
    checkpoint_ref: str
