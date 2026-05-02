from enum import Enum
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field

class ClaimFamily(str, Enum):
    policy_conformance_claim = "policy_conformance_claim"
    integrity_chain_claim = "integrity_chain_claim"
    transparency_publication_claim = "transparency_publication_claim"
    inclusion_coverage_claim = "inclusion_coverage_claim"
    witness_quorum_claim = "witness_quorum_claim"
    redaction_safety_claim = "redaction_safety_claim"
    profile_isolation_claim = "profile_isolation_claim"
    challenge_intake_safety_claim = "challenge_intake_safety_claim"
    drift_cleanliness_claim = "drift_cleanliness_claim"
    activation_readiness_claim = "activation_readiness_claim"
    rollback_readiness_claim = "rollback_readiness_claim"
    federated_precedence_claim = "federated_precedence_claim"
    external_input_quarantine_claim = "external_input_quarantine_claim"
    notarization_alignment_claim = "notarization_alignment_claim"
    e2e_promotion_claim = "e2e_promotion_claim"

class ClaimType(str, Enum):
    satisfied = "satisfied"
    conditionally_satisfied = "conditionally_satisfied"
    unsupported = "unsupported"
    stale = "stale"
    blocked = "blocked"
    unverifiable = "unverifiable"
    expired = "expired"
    superseded = "superseded"

class SupportStrength(str, Enum):
    high = "high"
    medium = "medium"
    low = "low"
    speculative = "speculative"
    none = "none"

class AttestationIssuerFamily(str, Enum):
    conformance_runner_attester = "conformance_runner_attester"
    integrity_verifier_attester = "integrity_verifier_attester"
    transparency_verifier_attester = "transparency_verifier_attester"
    witness_mesh_attester = "witness_mesh_attester"
    publication_safety_attester = "publication_safety_attester"
    portal_profile_attester = "portal_profile_attester"
    federated_governance_attester = "federated_governance_attester"
    multi_signer_trust_attester = "multi_signer_trust_attester"
    external_exchange_attester = "external_exchange_attester"

class AttestationStatus(str, Enum):
    valid = "valid"
    valid_with_caveats = "valid_with_caveats"
    stale = "stale"
    invalid = "invalid"
    revoked = "revoked"
    superseded = "superseded"
    unverifiable = "unverifiable"

class EnvelopeStatus(str, Enum):
    assurance_ready = "assurance_ready"
    assurance_ready_with_caveats = "assurance_ready_with_caveats"
    assurance_blocked = "assurance_blocked"
    assurance_stale = "assurance_stale"
    assurance_review_required = "assurance_review_required"
    assurance_superseded = "assurance_superseded"

class GateOutcome(str, Enum):
    pass_ = "pass"
    pass_with_caveats = "pass_with_caveats"
    review_required = "review_required"
    blocked = "blocked"
    blocked_critical = "blocked_critical"

class ClaimFreshnessRecord(BaseModel):
    evaluated_at: datetime = Field(default_factory=datetime.utcnow)
    is_stale: bool = False
    freshness_score: float = 1.0

class ClaimValidityWindowRecord(BaseModel):
    valid_from: datetime = Field(default_factory=datetime.utcnow)
    valid_until: Optional[datetime] = None

class AssuranceClaimRecord(BaseModel):
    claim_id: str
    claim_family: ClaimFamily
    claim_type: ClaimType
    target_family: str
    target_ref: str
    claim_statement: str
    machine_checkable_status: bool
    support_strength: SupportStrength
    freshness: ClaimFreshnessRecord = Field(default_factory=ClaimFreshnessRecord)
    validity_window: ClaimValidityWindowRecord = Field(default_factory=ClaimValidityWindowRecord)
    dependency_refs: List[str] = Field(default_factory=list)
    evidence_refs: List[str] = Field(default_factory=list)
    proof_refs: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)

class ProofCarryingBundleRecord(BaseModel):
    proof_bundle_id: str
    bundle_family: str
    target_ref: str
    carried_claim_refs: List[str] = Field(default_factory=list)
    evidence_refs: List[str] = Field(default_factory=list)
    proof_refs: List[str] = Field(default_factory=list)
    spec_refs: List[str] = Field(default_factory=list)
    attestation_refs: List[str] = Field(default_factory=list)
    freshness_state: str = "fresh"
    validity_state: str = "valid"
    warnings: List[str] = Field(default_factory=list)

class AssuranceAttestationRecord(BaseModel):
    attestation_id: str
    attestation_family: AttestationIssuerFamily
    issuer_ref: str
    target_ref: str
    claim_refs: List[str]
    evidence_refs: List[str] = Field(default_factory=list)
    validity_window: ClaimValidityWindowRecord = Field(default_factory=ClaimValidityWindowRecord)
    freshness_state: ClaimFreshnessRecord = Field(default_factory=ClaimFreshnessRecord)
    attestation_status: AttestationStatus
    signature_or_proof_ref: Optional[str] = None
    warnings: List[str] = Field(default_factory=list)

class MachineCheckableReleaseClaimRecord(BaseModel):
    release_claim_id: str
    promotion_target_ref: str
    claim_set_ref: str
    required_claim_families: List[ClaimFamily]
    satisfied_claim_families: List[ClaimFamily]
    blocking_missing_claims: List[ClaimFamily]
    claim_verification_status: GateOutcome
    created_at: datetime = Field(default_factory=datetime.utcnow)
    warnings: List[str] = Field(default_factory=list)

class PromotionEnvelopeRecord(BaseModel):
    envelope_id: str
    target_ref: str
    required_claims_summary: Dict[str, Any]
    satisfied_claims: List[str]
    blocked_claims: List[str]
    proof_carrying_bundle_ref: str
    assurance_attestations: List[str]
    trust_signature_status: str
    drift_cleanliness: str
    conformance_summary: str
    final_assurance_decision: EnvelopeStatus
    replay_hints: Dict[str, str] = Field(default_factory=dict)
    validity_window: ClaimValidityWindowRecord = Field(default_factory=ClaimValidityWindowRecord)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ClaimReplayRecord(BaseModel):
    replay_id: str
    original_envelope_id: str
    replay_outcome: str # matched, mismatched, inconclusive
    mismatch_details: List[str] = Field(default_factory=list)
    computed_at: datetime = Field(default_factory=datetime.utcnow)
