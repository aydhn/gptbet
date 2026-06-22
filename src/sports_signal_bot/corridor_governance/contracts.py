from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel


class CorridorCatalogEntryRecord(BaseModel):
    catalog_entry_id: str
    corridor_ref: str
    source_region_ref: str
    target_region_ref: str
    treaty_ref: str
    allowed_lane_families: List[str]
    allowed_transfer_classes: List[str]
    continuity_requirement_summary: str
    translation_requirement_summary: str
    sovereignty_notes: str
    freshness_state: str
    supersession_state: str
    visibility_profile: str
    warnings: List[str]


class CorridorCatalogRecord(BaseModel):
    entries: List[CorridorCatalogEntryRecord]


class CorridorVisibilityRecord(BaseModel):
    corridor_ref: str
    visibility_profile: str


class CorridorDiscoverabilityRecord(BaseModel):
    corridor_ref: str
    discoverability_status: str


class CorridorInteroperabilityHintRecord(BaseModel):
    corridor_ref: str
    interoperability_band: str
    major_caveats: List[str]


class CorridorCatalogDecisionRecord(BaseModel):
    corridor_ref: str
    decision: str
    rationale: str


class CorridorCatalogWarningRecord(BaseModel):
    corridor_ref: str
    warning_type: str
    message: str


class ContinuityAttestationInputRecord(BaseModel):
    attestation_id: str
    continuity_session_ref: str
    corridor_ref: str
    treaty_ref: str
    source_region_ref: str
    target_region_ref: str
    attestation_family: str
    attested_dimensions: List[str]
    attestation_status: str
    validity_window: Dict[str, str]
    caveat_refs: List[str]
    evidence_refs: List[str]
    warnings: List[str]


class ContinuityAttestationRecord(BaseModel):
    continuity_attestation_id: str
    continuity_session_ref: str
    corridor_ref: str
    treaty_ref: str
    source_region_ref: str
    target_region_ref: str
    attestation_family: str
    attested_dimensions: List[str]
    attestation_status: str
    validity_window: Dict[str, str]
    caveat_refs: List[str]
    evidence_refs: List[str]
    warnings: List[str]


class AttestationScopeRecord(BaseModel):
    attestation_id: str
    scope_details: str


class AttestationValidityRecord(BaseModel):
    attestation_id: str
    is_valid: bool
    reason: str


class AttestationContinuityLinkRecord(BaseModel):
    attestation_id: str
    continuity_session_ref: str


class AttestationCaveatRecord(BaseModel):
    caveat_id: str
    description: str
    severity: str


class AttestationIssuerRecordV2(BaseModel):
    issuer_id: str
    issuer_type: str


class AttestationVerificationRecord(BaseModel):
    attestation_id: str
    verified_at: datetime
    verified_by: str


class ContinuityAttestationManifestRecord(BaseModel):
    attestations: List[ContinuityAttestationRecord]


class AttestationSupersessionRecord(BaseModel):
    old_attestation_id: str
    new_attestation_id: str
    reason: str


class TreatyLifecycleStateRecord(BaseModel):
    treaty_ref: str
    lifecycle_state: str
    effective_from: datetime
    effective_until: Optional[datetime] = None
    renewal_due_at: Optional[datetime] = None
    superseded_by: Optional[str] = None
    termination_reason: Optional[str] = None
    warnings: List[str]


class TreatyLifecycleControllerRecord(BaseModel):
    states: List[TreatyLifecycleStateRecord]


class TreatyLifecycleTransitionRecord(BaseModel):
    treaty_ref: str
    from_state: str
    to_state: str
    transition_time: datetime


class TreatyRenewalRecord(BaseModel):
    treaty_ref: str
    renewal_time: datetime


class TreatyExpiryRecord(BaseModel):
    treaty_ref: str
    expiry_time: datetime


class TreatySupersessionRecordV2(BaseModel):
    old_treaty_ref: str
    new_treaty_ref: str


class TreatyFreshnessRecord(BaseModel):
    treaty_ref: str
    freshness_status: str


class TreatyLifecycleDecisionRecord(BaseModel):
    treaty_ref: str
    decision: str
    rationale: str


class TreatyLifecycleWarningRecord(BaseModel):
    treaty_ref: str
    message: str


class TreatyLifecycleAuditRecord(BaseModel):
    treaty_ref: str
    audit_time: datetime


class SovereignInteroperabilityScorecardInputRecord(BaseModel):
    scorecard_id: str
    scored_scope: str
    scored_corridor_refs: List[str]
    scored_treaty_refs: List[str]
    region_pair_ref: str
    dimension_scores: Dict[str, float]
    overall_score: float
    overall_band: str
    caveat_summary: List[str]
    blocking_gaps: List[str]
    warnings: List[str]


class SovereignInteroperabilityScorecardRecord(BaseModel):
    scorecard_id: str
    scored_scope: str
    scored_corridor_refs: List[str]
    scored_treaty_refs: List[str]
    region_pair_ref: str
    dimension_scores: Dict[str, float]
    overall_score: float
    overall_band: str
    caveat_summary: List[str]
    blocking_gaps: List[str]
    warnings: List[str]


class ScorecardDimensionRecord(BaseModel):
    dimension_name: str
    score: float


class ScorecardWeightRecord(BaseModel):
    dimension_name: str
    weight: float


class ScorecardPenaltyRecord(BaseModel):
    penalty_type: str
    deduction: float


class ScorecardExplanationRecord(BaseModel):
    scorecard_id: str
    explanation: str


class ScorecardTrendRecord(BaseModel):
    scorecard_id: str
    trend: str


class ScorecardGapRecord(BaseModel):
    scorecard_id: str
    gap_description: str


class InteroperabilityBenchmarkRecord(BaseModel):
    benchmark_id: str
    target_score: float


class RegionalInteroperabilitySummaryRecord(BaseModel):
    region_pair_ref: str
    summary: str
