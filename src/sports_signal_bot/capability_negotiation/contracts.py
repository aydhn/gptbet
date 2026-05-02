from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from enum import Enum
from datetime import datetime

class NegotiationStatus(str, Enum):
    negotiation_opened = "negotiation_opened"
    awaiting_response = "awaiting_response"
    partially_matched = "partially_matched"
    fully_matched = "fully_matched"
    matched_with_caveats = "matched_with_caveats"
    blocked_incompatible = "blocked_incompatible"
    review_required = "review_required"
    quarantined_unknown_profile = "quarantined_unknown_profile"
    superseded = "superseded"
    expired = "expired"

class NegotiationDecision(str, Enum):
    accept_profile = "accept_profile"
    accept_with_translation = "accept_with_translation"
    accept_review_only = "accept_review_only"
    reject_incompatible = "reject_incompatible"
    quarantine_pending_manual_review = "quarantine_pending_manual_review"
    narrow_scope_and_retry = "narrow_scope_and_retry"
    downgrade_to_minimal_interop = "downgrade_to_minimal_interop"
    require_portable_spec_bundle = "require_portable_spec_bundle"

class DimensionOutcome(str, Enum):
    exact_match = "exact_match"
    compatible_with_translation = "compatible_with_translation"
    narrower_support = "narrower_support"
    unsupported = "unsupported"
    conflicting = "conflicting"
    unknown = "unknown"

class SpecPortabilityClass(str, Enum):
    fully_portable = "fully_portable"
    portable_with_redactions = "portable_with_redactions"
    portable_with_semantic_notes = "portable_with_semantic_notes"
    review_only_portable = "review_only_portable"
    nonportable_internal_only = "nonportable_internal_only"

class ReplayOutcome(str, Enum):
    replay_matched = "replay_matched"
    replay_changed_due_to_new_policy = "replay_changed_due_to_new_policy"
    replay_invalid_missing_context = "replay_invalid_missing_context"
    replay_stale_profile = "replay_stale_profile"
    replay_conflict_detected = "replay_conflict_detected"

class DriftOutcome(str, Enum):
    compatible_drift = "compatible_drift"
    caution_drift = "caution_drift"
    review_required_drift = "review_required_drift"
    blocking_drift = "blocking_drift"
    federation_breaking_drift = "federation_breaking_drift"

class CapabilityTrustConstraintRecord(BaseModel):
    constraint_id: str
    description: str

class CapabilityProfileRecord(BaseModel):
    profile_id: str
    registry_or_verifier_ref: str
    supported_artifact_families: List[str] = Field(default_factory=list)
    supported_claim_families: List[str] = Field(default_factory=list)
    supported_spec_families: List[str] = Field(default_factory=list)
    supported_versions: List[str] = Field(default_factory=list)
    supported_proof_formats: List[str] = Field(default_factory=list)
    supported_replay_modes: List[str] = Field(default_factory=list)
    supported_notarization_types: List[str] = Field(default_factory=list)
    supported_translation_modes: List[str] = Field(default_factory=list)
    supported_redaction_profiles: List[str] = Field(default_factory=list)
    trust_constraints: List[CapabilityTrustConstraintRecord] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)

class CapabilityOfferRecord(BaseModel):
    offer_id: str
    profile: CapabilityProfileRecord
    target_registry_ref: str

class CapabilityResponseRecord(BaseModel):
    response_id: str
    offer_ref: str
    profile: CapabilityProfileRecord

class TranslationNeedRecord(BaseModel):
    family: str
    translation_rule: str

class NarrowingConstraintRecord(BaseModel):
    family: str
    narrowed_to: List[str]

class CapabilityGapRecord(BaseModel):
    dimension: str
    gap_description: str

class NegotiationDimensionResultRecord(BaseModel):
    dimension: str
    outcome: DimensionOutcome
    notes: str

class CapabilityDiffRecord(BaseModel):
    dimensions: List[NegotiationDimensionResultRecord]
    gaps: List[CapabilityGapRecord]
    translation_needs: List[TranslationNeedRecord]
    narrowing_constraints: List[NarrowingConstraintRecord]

class NegotiatedScopeRecord(BaseModel):
    allowed_artifact_families: List[str]
    allowed_claim_families: List[str]
    allowed_proof_formats: List[str]
    allowed_notarization_modes: List[str]

class NegotiatedTranslationRuleRecord(BaseModel):
    rule_id: str
    source_family: str
    target_family: str

class NegotiatedReplayPolicyRecord(BaseModel):
    replay_requirement_profile: str

class NegotiatedTrustRecord(BaseModel):
    accepted_trust_lanes: List[str]
    import_export_boundaries: List[str]
    redaction_publication_restrictions: List[str]

class NegotiatedProfileRecord(BaseModel):
    negotiated_profile_id: str
    source_profile_ref: str
    target_profile_ref: str
    scope: NegotiatedScopeRecord
    translations: List[NegotiatedTranslationRuleRecord]
    replay_policy: NegotiatedReplayPolicyRecord
    trust: NegotiatedTrustRecord
    expiry: Optional[str] = None
    supersession: Optional[str] = None

class CapabilityNegotiationRecord(BaseModel):
    negotiation_id: str
    source_profile_ref: str
    target_profile_ref: str
    requested_capabilities: List[str]
    offered_capabilities: List[str]
    matched_capabilities: List[str]
    rejected_capabilities: List[str]
    negotiated_profile_ref: Optional[str] = None
    negotiation_status: NegotiationStatus
    created_at: str
    warnings: List[str] = Field(default_factory=list)

class PortableAssertionRecord(BaseModel):
    assertion_id: str
    semantics: str

class SpecSemanticTagRecord(BaseModel):
    tag: str
    description: str

class SpecExportConstraintRecord(BaseModel):
    constraint: str

class SpecBundleTranslationHintRecord(BaseModel):
    hint: str

class PortableSpecBundleRecord(BaseModel):
    spec_bundle_id: str
    bundle_family: str
    portable_profile: SpecPortabilityClass
    included_specs: List[str]
    included_assertions: List[PortableAssertionRecord]
    version_matrix: Dict[str, str]
    compatibility_notes: List[str]
    export_constraints: List[SpecExportConstraintRecord]
    redaction_profile: str
    notarization_refs: Optional[List[str]] = None
    warnings: List[str] = Field(default_factory=list)
    semantic_tags: List[SpecSemanticTagRecord] = Field(default_factory=list)
    translation_hints: List[SpecBundleTranslationHintRecord] = Field(default_factory=list)

class RegistrySnapshotDigestRecord(BaseModel):
    snapshot_id: str
    digest: str

class RegistryNotaryReceiptRecord(BaseModel):
    receipt_id: str
    signature: str

class NotarizedRegistryViewRecord(BaseModel):
    view_id: str
    snapshot_digest: RegistrySnapshotDigestRecord
    receipt: RegistryNotaryReceiptRecord

class RegistrySnapshotNotarizationRecord(BaseModel):
    notarization_id: str
    registry_ref: str
    view: NotarizedRegistryViewRecord
    created_at: str

class FederationVerifierClassRecord(BaseModel):
    class_id: str
    description: str

class FederationAcceptanceRuleRecord(BaseModel):
    rule_id: str
    description: str

class FederationReviewRequirementRecord(BaseModel):
    requirement_id: str
    description: str

class FederationDowngradeRuleRecord(BaseModel):
    rule_id: str
    description: str

class FederationPolicyRecord(BaseModel):
    policy_id: str
    verifier_classes: List[FederationVerifierClassRecord]
    acceptance_rules: List[FederationAcceptanceRuleRecord]
    review_requirements: List[FederationReviewRequirementRecord]
    downgrade_rules: List[FederationDowngradeRuleRecord]

class VerifierOnboardingRecord(BaseModel):
    onboarding_id: str
    verifier_ref: str
    profile: CapabilityProfileRecord
    status: str

class RegistryCapabilityManifest(BaseModel):
    manifest_id: str
    profiles: List[CapabilityProfileRecord]
    negotiations: List[CapabilityNegotiationRecord]
    portable_bundles: List[PortableSpecBundleRecord]
    notarizations: List[RegistrySnapshotNotarizationRecord]
    drifts: List[Dict[str, Any]]
    onboardings: List[VerifierOnboardingRecord]
    summary: Dict[str, Any]
