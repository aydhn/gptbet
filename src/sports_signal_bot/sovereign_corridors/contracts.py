from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class SovereignRuntimeCorridorRecord(BaseModel):
    corridor_id: str
    corridor_family: str
    source_region_ref: str
    target_region_ref: str
    treaty_ref: Optional[str] = None
    sovereignty_policy_refs: List[str] = Field(default_factory=list)
    allowed_lane_families: List[str] = Field(default_factory=list)
    allowed_transfer_classes: List[str] = Field(default_factory=list)
    corridor_status: str
    warnings: List[str] = Field(default_factory=list)

class CorridorDefinitionRecord(BaseModel):
    corridor_family: str
    description: str

class CorridorBoundaryRecord(BaseModel):
    source_region: str
    target_region: str

class CorridorEligibilityRecord(BaseModel):
    eligible: bool
    reasons: List[str]

class CorridorEntryRecord(BaseModel):
    corridor_ref: str
    transfer_class: str
    status: str

class CorridorExitRecord(BaseModel):
    corridor_ref: str
    status: str

class CorridorCheckpointRecord(BaseModel):
    checkpoint_id: str
    status: str

class CorridorGuardRecord(BaseModel):
    guard_id: str
    outcome: str
    messages: List[str]

class TreatyBackedRemediationCorridorRecord(BaseModel):
    treaty_ref: str
    corridor_ref: str
    limitations: Dict[str, Any]

class PolicyBorderTranslationLedgerRecord(BaseModel):
    ledger_id: str
    source_region_ref: str
    target_region_ref: str
    translation_entries: List[Dict[str, Any]] = Field(default_factory=list)
    active_mappings: List[str] = Field(default_factory=list)
    superseded_mappings: List[str] = Field(default_factory=list)
    integrity_refs: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)

class TranslationLedgerEntryRecord(BaseModel):
    entry_id: str
    source_element: str
    target_element: str
    mapping_rule: str
    loss_class: str

class TranslationMappingRecord(BaseModel):
    mapping_id: str
    source: str
    target: str

class TranslationLossRecord(BaseModel):
    loss_class: str
    description: str

class TranslationIntegrityRecord(BaseModel):
    hash: str

class RegionalAssuranceContinuityControllerRecord(BaseModel):
    controller_id: str
    controller_family: str
    monitored_corridor_refs: List[str] = Field(default_factory=list)
    continuity_policy_ref: str
    required_checkpoint_families: List[str] = Field(default_factory=list)
    gap_thresholds: Dict[str, str] = Field(default_factory=dict)
    decision_status: str
    warnings: List[str] = Field(default_factory=list)

class ContinuitySessionRecord(BaseModel):
    session_id: str
    status: str

class ContinuityCheckpointRecord(BaseModel):
    checkpoint_id: str
    status: str

class ContinuityGapRecord(BaseModel):
    gap_id: str
    severity: str

class ContinuityDecisionRecord(BaseModel):
    decision_id: str
    outcome: str

class CorridorHealthRecord(BaseModel):
    corridor_ref: str
    health_status: str
    metrics: Dict[str, Any]

class CorridorManifest(BaseModel):
    manifest_id: str
    generated_at: datetime
    corridors: List[SovereignRuntimeCorridorRecord]

class CorridorWarningRecord(BaseModel):
    warning: str

class CorridorAuditRecord(BaseModel):
    audit_id: str
    timestamp: datetime

class CorridorTreatyScopeRecord(BaseModel):
    scope_id: str

class CorridorTreatyConstraintRecord(BaseModel):
    constraint_id: str

class CorridorTreatyReviewRequirementRecord(BaseModel):
    requirement_id: str

class CorridorTreatyVisibilityRuleRecord(BaseModel):
    rule_id: str

class BorderTranslationRuleRecord(BaseModel):
    rule_id: str

class TranslationSemanticClassRecord(BaseModel):
    semantic_class: str

class TranslationConstraintRecord(BaseModel):
    constraint_id: str

class TranslationReplayRecord(BaseModel):
    replay_id: str
    outcome: str

class ContinuityRequirementRecord(BaseModel):
    requirement_id: str

class ContinuityEvidenceRecord(BaseModel):
    evidence_id: str

class ContinuityRecoveryHintRecord(BaseModel):
    hint: str

class ContinuitySeverityRecord(BaseModel):
    severity: str

class CorridorListingVisibilityRecord(BaseModel):
    listing_id: str

class ListingTranslationHintRecord(BaseModel):
    hint: str

class ListingContinuityRequirementRecord(BaseModel):
    requirement: str

class ListingCorridorEligibilityRecord(BaseModel):
    eligibility: str
