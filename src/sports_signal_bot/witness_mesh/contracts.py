import datetime
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from enum import Enum

class WitnessFamily(str, Enum):
    LOCAL_WITNESS = "local_witness"
    MIRROR_WITNESS = "mirror_witness"
    FEDERATED_PLANE_WITNESS = "federated_plane_witness"
    AUDIT_SNAPSHOT_WITNESS = "audit_snapshot_witness"
    REVIEW_QUARANTINE_WITNESS = "review_quarantine_witness"
    EXTERNAL_STYLE_PLACEHOLDER_WITNESS = "external_style_placeholder_witness"
    CHALLENGE_ONLY_WITNESS = "challenge_only_witness"

class WitnessCapability(str, Enum):
    VERIFY_CHECKPOINT = "verify_checkpoint"
    VERIFY_INCLUSION = "verify_inclusion"
    VERIFY_CONSISTENCY = "verify_consistency"
    VERIFY_MIRROR_SYNC = "verify_mirror_sync"
    VERIFY_DECISION_PUBLICATION = "verify_decision_publication"
    VERIFY_IMPORT_CLAIM = "verify_import_claim"
    ISSUE_CHALLENGE = "issue_challenge"
    ANSWER_CHALLENGE = "answer_challenge"
    COUNTERSIGN_WITNESS_STATEMENT = "countersign_witness_statement"
    OBSERVE_GOSSIP = "observe_gossip"

class WitnessNodeRecord(BaseModel):
    witness_id: str
    witness_name: str
    witness_family: WitnessFamily
    trust_role: str
    verification_capabilities: List[WitnessCapability]
    observed_log_families: List[str]
    mirror_refs: List[str] = Field(default_factory=list)
    active_status: str
    freshness_window: Dict[str, Any]
    warnings: List[str] = Field(default_factory=list)

class WitnessStatementType(str, Enum):
    CHECKPOINT_SEEN = "checkpoint_seen"
    CHECKPOINT_VERIFIED = "checkpoint_verified"
    INCLUSION_VERIFIED = "inclusion_verified"
    CONSISTENCY_VERIFIED = "consistency_verified"
    MIRROR_DIVERGENCE_CONFIRMED = "mirror_divergence_confirmed"
    MIRROR_DIVERGENCE_REJECTED = "mirror_divergence_rejected"
    BUNDLE_PUBLICATION_CONFIRMED = "bundle_publication_confirmed"
    DECISION_PROOF_PUBLICATION_CONFIRMED = "decision_proof_publication_confirmed"
    SIGNER_REVOCATION_SEEN = "signer_revocation_seen"
    OVERRIDE_EXPIRY_CONFIRMED = "override_expiry_confirmed"
    ANOMALY_OBSERVED = "anomaly_observed"
    ANOMALY_NOT_OBSERVED = "anomaly_not_observed"
    CHALLENGE_ISSUED = "challenge_issued"
    CHALLENGE_ANSWERED = "challenge_answered"

class WitnessStatementRecord(BaseModel):
    statement_id: str
    witness_id: str
    statement_family: WitnessStatementType
    target_ref: str
    target_hash: str
    observed_status: str
    observation_window: Dict[str, Any]
    verification_result: str
    proof_refs: List[str] = Field(default_factory=list)
    created_at: datetime.datetime
    warnings: List[str] = Field(default_factory=list)

class ChallengeStatus(str, Enum):
    CHALLENGE_OPENED = "challenge_opened"
    AWAITING_RESPONSE = "awaiting_response"
    RESPONSE_RECEIVED = "response_received"
    RESPONSE_VALIDATED = "response_validated"
    RESOLVED_CONFIRMED = "resolved_confirmed"
    RESOLVED_REJECTED = "resolved_rejected"
    UNRESOLVED_ESCALATED = "unresolved_escalated"
    EXPIRED_NO_RESPONSE = "expired_no_response"
    SUPERSEDED = "superseded"

class ChallengeRecord(BaseModel):
    challenge_id: str
    challenge_family: str
    target_ref: str
    origin_witness_id: str
    anomaly_ref: Optional[str] = None
    asserted_issue: str
    expected_response_type: str
    severity: str
    deadline: datetime.datetime
    current_status: ChallengeStatus
    warnings: List[str] = Field(default_factory=list)

class WitnessCoverageRecord(BaseModel):
    coverage_id: str
    target_ref: str
    witness_ids: List[str]
    covered: bool

class WitnessMeshManifest(BaseModel):
    manifest_id: str
    nodes: List[WitnessNodeRecord]
    created_at: datetime.datetime

class WitnessDisagreementSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class WitnessConsensusType(str, Enum):
    UNANIMOUS_CONFIRMED = "unanimous_confirmed"
    MAJORITY_CONFIRMED = "majority_confirmed"
    SPLIT_OBSERVATION = "split_observation"
    INSUFFICIENT_WITNESSES = "insufficient_witnesses"
    STALE_CONSENSUS = "stale_consensus"
    CONTESTED = "contested"

class WitnessConsensusRecord(BaseModel):
    consensus_id: str
    target_ref: str
    consensus_type: WitnessConsensusType
    supporting_witness_ids: List[str]
    dissenting_witness_ids: List[str]
    created_at: datetime.datetime

class TransparencyAnomalyType(str, Enum):
    MISSING_EXPECTED_PUBLICATION = "missing_expected_publication"
    INCONSISTENT_CHECKPOINT_CLAIM = "inconsistent_checkpoint_claim"
    BROKEN_INCLUSION_PATH = "broken_inclusion_path"
    BROKEN_CONSISTENCY_PATH = "broken_consistency_path"
    MIRROR_DIVERGENCE = "mirror_divergence"
    ORPHAN_DECISION_PUBLICATION = "orphan_decision_publication"
    PUBLICATION_WITHOUT_EXPECTED_SIGNER_TRUST = "publication_without_expected_signer_trust"
    SIGNER_REVOCATION_PUBLICATION_GAP = "signer_revocation_publication_gap"
    IMPORTED_BUNDLE_PUBLICATION_GAP = "imported_bundle_publication_gap"
    STALE_CHECKPOINT_VISIBILITY_GAP = "stale_checkpoint_visibility_gap"
    CONTRADICTORY_WITNESS_REPORTS = "contradictory_witness_reports"
    UNEXPECTED_LOG_REWRITE_SIGNAL = "unexpected_log_rewrite_signal"

class TransparencyAnomalyRecord(BaseModel):
    anomaly_id: str
    anomaly_type: TransparencyAnomalyType
    target_ref: str
    severity: str
    detected_by_witness_ids: List[str]
    created_at: datetime.datetime

class AnomalyAdjudicationOutcome(str, Enum):
    BENIGN_EXPLAINED = "benign_explained"
    LOCAL_MIRROR_ISSUE = "local_mirror_issue"
    SOURCE_TRANSPARENCY_ISSUE = "source_transparency_issue"
    STALE_STATE_MISUNDERSTANDING = "stale_state_misunderstanding"
    INTEGRITY_BREAK_CONFIRMED = "integrity_break_confirmed"
    QUARANTINE_REQUIRED = "quarantine_required"
    FREEZE_RECOMMENDED = "freeze_recommended"
    SIGNER_TRUST_REVIEW_REQUIRED = "signer_trust_review_required"
    GOVERNANCE_HOLD_REQUIRED = "governance_hold_required"
    UNRESOLVED_MONITOR = "unresolved_monitor"

class AnomalyAdjudicationRecord(BaseModel):
    adjudication_id: str
    anomaly_id: str
    outcome: AnomalyAdjudicationOutcome
    rationale: str
    created_at: datetime.datetime

class ReadinessStatus(str, Enum):
    NOT_READY = "not_ready"
    MINIMALLY_READY = "minimally_ready"
    PARTIALLY_READY = "partially_ready"
    STRONG_INTERNAL_READINESS = "strong_internal_readiness"
    PUBLIC_STYLE_READINESS_CANDIDATE = "public_style_readiness_candidate"

class PublicStyleReadinessRecord(BaseModel):
    readiness_id: str
    status: ReadinessStatus
    dimension_scores: Dict[str, float]
    blockers: List[str]
    created_at: datetime.datetime
