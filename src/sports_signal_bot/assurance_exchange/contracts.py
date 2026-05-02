from enum import Enum
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field
from sports_signal_bot.assurance.contracts import ClaimFamily, AttestationStatus, ClaimValidityWindowRecord, ClaimFreshnessRecord, GateOutcome

# Ensure dict handles pydantic objects correctly by doing default factory mapping

class AssuranceExchangePacketRecord(BaseModel):
    exchange_packet_id: str
    packet_family: str
    source_registry_ref: str
    target_registry_ref: Optional[str] = None
    carried_bundle_refs: List[str] = Field(default_factory=list)
    claim_refs: List[str] = Field(default_factory=list)
    attestation_refs: List[str] = Field(default_factory=list)
    proof_refs: List[str] = Field(default_factory=list)
    translation_refs: Optional[List[str]] = Field(default_factory=list)
    notarization_refs: Optional[List[str]] = Field(default_factory=list)
    validity_window: ClaimValidityWindowRecord = Field(default_factory=ClaimValidityWindowRecord)
    warnings: List[str] = Field(default_factory=list)

class FederatedRegistryRecord(BaseModel):
    registry_id: str
    registry_name: str
    registry_family: str
    trust_domain: str
    supported_artifact_families: List[str] = Field(default_factory=list)
    supported_claim_families: List[ClaimFamily] = Field(default_factory=list)
    active_status: bool
    compatibility_profile: str
    sync_mode: str
    warnings: List[str] = Field(default_factory=list)

class NotarizedPromotionEnvelopeRecord(BaseModel):
    notarized_envelope_id: str
    promotion_envelope_ref: str
    digest_ref: str
    notarization_ref: str
    publication_scope: str
    exchange_visibility_profile: str
    validity_window: ClaimValidityWindowRecord = Field(default_factory=ClaimValidityWindowRecord)
    verification_status: str
    warnings: List[str] = Field(default_factory=list)

class RegistryNodeRecord(BaseModel):
    node_id: str
    registry_id: str
    status: str

class RegistryFederationLinkRecord(BaseModel):
    link_id: str
    source_registry: str
    destination_registry: str
    allowed_artifact_families: List[str] = Field(default_factory=list)
    allowed_claim_families: List[ClaimFamily] = Field(default_factory=list)
    translation_policy: str
    trust_policy: str
    notarization_policy: str
    quarantine_rules: Dict[str, Any] = Field(default_factory=dict)
    sync_mode: str
    approval_requirements: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)

class AssuranceInteroperabilityRecord(BaseModel):
    record_id: str
    packet_id: str
    status: str

class ClaimTranslationRecord(BaseModel):
    translation_id: str
    source_claim_family: ClaimFamily
    destination_claim_family: ClaimFamily
    mapping_type: str
    semantic_loss_risk: str
    strengthened_or_weakened: str
    added_caveats: List[str] = Field(default_factory=list)
    required_verification_steps: List[str] = Field(default_factory=list)
    accepted_profiles: List[str] = Field(default_factory=list)

class CompatibilityMatrixRecord(BaseModel):
    matrix_id: str
    name: str

class InteropVerificationRecord(BaseModel):
    verification_id: str
    status: str

class PromotionEnvelopeExchangeRecord(BaseModel):
    exchange_id: str
    envelope_id: str
    status: str

class ExternalRegistryImportRecord(BaseModel):
    import_id: str
    registry_id: str
    status: str

class ExternalRegistryExportRecord(BaseModel):
    export_id: str
    registry_id: str
    status: str

class RegistrySnapshotRecord(BaseModel):
    snapshot_id: str
    registry_id: str
    signed_snapshot_manifest: str
    exported_artifact_list: List[str] = Field(default_factory=list)
    claim_coverage_summary: Dict[str, Any] = Field(default_factory=dict)
    trust_and_compatibility_metadata: Dict[str, Any] = Field(default_factory=dict)
    incremental_sync_hints: Dict[str, Any] = Field(default_factory=dict)
    supersession_map: Dict[str, str] = Field(default_factory=dict)
    revocation_map: Dict[str, str] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    validity: str

class CrossSystemReplayRecord(BaseModel):
    replay_id: str
    packet_id: str
    result: str # replay_accepted, replay_accepted_with_caveats, replay_review_required, replay_quarantined, replay_rejected
    details: str

class AssuranceInteroperabilityManifest(BaseModel):
    manifest_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class FederationTrustRecord(BaseModel):
    trust_id: str
    registry_id: str
    trust_policy: str

class RegistrySyncRecord(BaseModel):
    sync_id: str
    registry_id: str
    status: str # sync_clean, sync_partial, sync_quarantined, sync_conflicted, sync_stale, sync_blocked

class AssuranceQuarantineRecord(BaseModel):
    quarantine_id: str
    packet_id: str
    reason: str
    status: str

class RegistryCapabilityRecord(BaseModel):
    capability_id: str
    registry_id: str

class RegistryScopeRecord(BaseModel):
    scope_id: str
    registry_id: str

class RegistrySyncPolicyRecord(BaseModel):
    policy_id: str
    registry_id: str

class RegistryTrustBoundaryRecord(BaseModel):
    boundary_id: str
    registry_id: str

class RegistryHealthRecord(BaseModel):
    health_id: str
    registry_id: str

class ClaimInteropProfileRecord(BaseModel):
    profile_id: str

class ClaimSemanticClassRecord(BaseModel):
    class_id: str

class ClaimPortabilityRecord(BaseModel):
    portability_id: str

class MatrixCellRecord(BaseModel):
    cell_id: str

class CompatibilityDecisionRecord(BaseModel):
    decision_id: str

class CompatibilityGapRecord(BaseModel):
    gap_id: str

class TranslationRequirementRecord(BaseModel):
    requirement_id: str

class ReplayInputRecord(BaseModel):
    input_id: str

class ReplayContextMappingRecord(BaseModel):
    mapping_id: str

class ReplayTranslationRecord(BaseModel):
    translation_id: str

class ReplayDecisionRecord(BaseModel):
    decision_id: str

class ReplayMismatchRecord(BaseModel):
    mismatch_id: str

class QuarantineReasonRecord(BaseModel):
    reason_id: str

class QuarantineReleaseConditionRecord(BaseModel):
    condition_id: str
