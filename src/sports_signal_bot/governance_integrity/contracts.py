from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime
from enum import Enum

class TrustLevel(str, Enum):
    DEV = "dev"
    REVIEW = "review"
    ACTIVE = "active"
    EMERGENCY = "emergency"
    REVOKED = "revoked"

class SignerStatus(str, Enum):
    ACTIVE = "active"
    LIMITED = "limited"
    REVIEW_ONLY = "review_only"
    SUSPENDED = "suspended"
    REVOKED = "revoked"
    EXPIRED = "expired"

class BundleStatus(str, Enum):
    DRAFT_UNSIGNED = "draft_unsigned"
    DRAFT_SIGNED = "draft_signed"
    REVIEW_VERIFIED = "review_verified"
    CANDIDATE_DISTRIBUTION_READY = "candidate_distribution_ready"
    ACTIVE_VERIFIED = "active_verified"
    DEPRECATED = "deprecated"
    REVOKED = "revoked"
    QUARANTINED = "quarantined"

class VerificationStatus(str, Enum):
    VALID = "valid"
    INVALID_SIGNATURE = "invalid_signature"
    UNTRUSTED_SIGNER = "untrusted_signer"
    REVOKED_SIGNER = "revoked_signer"
    BROKEN_CHAIN = "broken_chain"
    MISSING_PROOF = "missing_proof"
    QUARANTINED = "quarantined"

class IntegrityMode(str, Enum):
    STRICT_ACTIVE = "strict_active_mode"
    REVIEW = "review_mode"
    DEV = "dev_mode"
    IMPORT_QUARANTINE = "import_quarantine_mode"

class SignerRecord(BaseModel):
    signer_id: str
    signer_family: str
    signer_name: str
    trust_level: TrustLevel
    active_status: SignerStatus
    key_ref_placeholder: str
    signing_scope: List[str]
    review_required: bool
    warnings: List[str] = Field(default_factory=list)

class SignatureRecord(BaseModel):
    signature_id: str
    signer_id: str
    signature_blob: str
    algorithm: str
    timestamp: datetime

class BundleManifestRecord(BaseModel):
    manifest_version: str = "1.0"
    bundle_family: str
    bundle_version: str
    payload_hash: str
    created_at: datetime
    dependencies: List[str] = Field(default_factory=list)

class SignedBundleRecord(BaseModel):
    signed_bundle_id: str
    bundle_family: str
    bundle_version: str
    bundle_hash: str
    manifest_hash: str
    signer_id: str
    signature_ref: str
    created_at: datetime
    scope: Dict[str, Any]
    status: BundleStatus
    warnings: List[str] = Field(default_factory=list)


class DecisionProofParameters(BaseModel):
    decision_family: str
    decision_ref: str
    applied_policy_snapshot_ref: str
    inputs: Dict[str, Any]
    outputs: Dict[str, Any]
    evidence_refs: List[str] = Field(default_factory=list)
    prior_proof_ref: Optional[str] = None

class DecisionProofRecord(BaseModel):

    decision_proof_id: str
    decision_family: str
    decision_ref: str
    applied_policy_snapshot_ref: str
    evidence_refs: List[str]
    input_hash: str
    output_hash: str
    proof_hash: str
    prior_proof_ref: Optional[str] = None
    signer_status: SignerStatus
    verification_status: VerificationStatus
    created_at: datetime
    warnings: List[str] = Field(default_factory=list)

class LedgerEntryRecord(BaseModel):
    entry_id: str
    timestamp: datetime
    event_family: str
    actor_metadata: Dict[str, Any]
    bundle_refs: List[str] = Field(default_factory=list)
    decision_refs: List[str] = Field(default_factory=list)
    proof_refs: List[str] = Field(default_factory=list)
    verification_status: VerificationStatus
    entry_hash: str
    previous_entry_hash: Optional[str] = None
    chain_hash: str
    redacted_payload: Dict[str, Any] = Field(default_factory=dict)

class LedgerChainRecord(BaseModel):
    chain_id: str
    tail_entry_hash: str
    entry_count: int
    is_intact: bool
    last_verified_at: datetime

class ProofLinkRecord(BaseModel):
    source_ref: str
    target_ref: str
    link_type: str

class BundlePackagingRecord(BaseModel):
    package_id: str
    package_type: str
    payload: Dict[str, Any]
    manifest: BundleManifestRecord
    signature_block: SignatureRecord
    parent_refs: List[str] = Field(default_factory=list)
    overlay_refs: List[str] = Field(default_factory=list)
    compatibility_notes: str = ""

class DistributionPackageRecord(BaseModel):
    distribution_id: str
    packaging_record: BundlePackagingRecord
    required_trust_level: TrustLevel
    import_instructions: str
    verification_summary: Dict[str, Any]

class ImportedBundleStateRecord(BaseModel):
    import_id: str
    package_id: str
    imported_at: datetime
    initial_status: BundleStatus
    quarantine_reason: Optional[str] = None

class IntegrityFailureRecord(BaseModel):
    failure_id: str
    timestamp: datetime
    severity: str
    reason: str
    affected_refs: List[str]
    context: Dict[str, Any]

class VerificationWarningRecord(BaseModel):
    warning_id: str
    timestamp: datetime
    message: str
    related_refs: List[str]

class GovernanceIntegrityManifest(BaseModel):
    manifest_id: str
    generated_at: datetime
    signed_bundle_count: int
    active_verified_count: int
    verification_failures: int
    quarantined_imports: int
    ledger_chain_intact: bool
    unsigned_dev_usage_count: int

class ImmutableReferenceRecord(BaseModel):
    ref_id: str
    ref_type: str
    target_hash: str
    created_at: datetime

class TrustPolicyRecord(BaseModel):
    policy_id: str
    allowed_signers_by_family: Dict[str, List[str]]
    minimum_trust_by_environment: Dict[str, TrustLevel]
    require_multi_review: bool
    allow_unsigned_dev: bool
