from datetime import datetime
from typing import List, Optional, Dict, Any, Set
from pydantic import BaseModel, Field

# -----------------------------------------------------------------------------
# REGISTRY CONTRACTS
# -----------------------------------------------------------------------------


class RegistryFreshnessRecord(BaseModel):
    last_verified_at: datetime
    valid_until: datetime
    is_stale: bool


class RegistryDecisionRecord(BaseModel):
    decision_type: str
    decision_reason: str
    decided_at: datetime
    decision_by: str


class RegistryValidationRecord(BaseModel):
    validated_at: datetime
    is_valid: bool
    errors: List[str] = Field(default_factory=list)


class RegistrySupersessionLinkRecord(BaseModel):
    superseded_by_ref: str
    supersession_reason: str
    superseded_at: datetime


class EntrySemanticVersionRecord(BaseModel):
    major: int
    minor: int
    patch: int
    build_metadata: Optional[str] = None


class EntrySupersessionReasonRecord(BaseModel):
    reason_code: str
    description: str


class VersionLineageRecord(BaseModel):
    previous_version_ref: Optional[str] = None
    next_version_refs: List[str] = Field(default_factory=list)


class CurrentnessDecisionRecord(BaseModel):
    is_current: bool
    caveats: List[str] = Field(default_factory=list)
    decided_at: datetime


class RegistryVersionRecord(BaseModel):
    version_id: str
    semantic_version: EntrySemanticVersionRecord
    issued_at: datetime
    policy_version_refs: List[str] = Field(default_factory=list)
    lineage: VersionLineageRecord


class RegistryEntryStateRecord(BaseModel):
    state: str  # drafted, reviewable, current, current_with_caveats, renewal_due, expired, superseded, suspended, archived
    state_reason: str
    updated_at: datetime


class RegistryEntryRecord(BaseModel):
    registry_entry_id: str
    entry_family: str  # corridor_entry, treaty_entry, etc.
    target_ref: str
    version_ref: str
    state_ref: RegistryEntryStateRecord
    lineage_refs: VersionLineageRecord
    discoverability_state: str
    freshness_state: RegistryFreshnessRecord
    supersession_state: Optional[RegistrySupersessionLinkRecord] = None
    warnings: List[str] = Field(default_factory=list)


class RegistryCurrentPointerRecord(BaseModel):
    pointer_id: str
    registry_family: str
    scope_ref: str
    current_entry_ref: str
    updated_at: datetime


class RegistryScopeRecord(BaseModel):
    scope_id: str
    description: str


class RegistryVisibilityRecordV2(BaseModel):
    visibility_level: str
    allowed_scopes: List[str] = Field(default_factory=list)


class RegistryHealthRecordV2(BaseModel):
    status: str  # healthy, caution, stale_pressure, supersession_stressed, attestation_gap_heavy, degraded, blocked
    stale_current_count: int = 0
    expired_entry_misuse_pressure: float = 0.0
    attestation_validity_coverage: float = 0.0
    last_evaluated_at: datetime


class RegistryWarningRecord(BaseModel):
    warning_code: str
    message: str
    severity: str


class CorridorRegistryRecord(BaseModel):
    registry_id: str
    registry_family: str  # sovereign_corridor_registry, treaty_registry, etc.
    owning_scope_ref: str
    registered_corridor_refs: List[str] = Field(default_factory=list)
    registered_treaty_refs: List[str] = Field(default_factory=list)
    registered_attestation_refs: List[str] = Field(default_factory=list)
    registered_baseline_refs: List[str] = Field(default_factory=list)
    current_pointer_refs: List[str] = Field(default_factory=list)
    health_status: RegistryHealthRecordV2
    warnings: List[RegistryWarningRecord] = Field(default_factory=list)


class CorridorRegistryManifestRecord(BaseModel):
    manifest_id: str
    generated_at: datetime
    registry_ref: str
    total_entries: int
    current_pointers_count: int


# -----------------------------------------------------------------------------
# CONTINUITY ATTESTATION EXCHANGE CONTRACTS
# -----------------------------------------------------------------------------


class AttestationExchangeScopeRecord(BaseModel):
    scope: str  # visibility_only, review_only, bounded_comparison, baseline_comparison_support, continuity_summary_only, no_runtime_authority, replay_evidence_support


class AttestationExchangeConstraintRecord(BaseModel):
    constraint_type: str
    constraint_value: str


class ExchangeCaveatRecord(BaseModel):
    caveat_code: str
    description: str


class ExchangeVerificationRecordV2(BaseModel):
    verified_at: datetime
    is_verified: bool
    verifier_ref: str


class ExchangeReplayRecord(BaseModel):
    replay_supported: bool
    replay_evidence_ref: Optional[str] = None


class AttestationExchangeDecisionRecord(BaseModel):
    decision: str
    reason: str


class AttestationExchangePacketRecord(BaseModel):
    exchange_packet_id: str
    source_registry_ref: str
    attestation_refs: List[str] = Field(default_factory=list)
    corridor_refs: List[str] = Field(default_factory=list)
    treaty_refs: List[str] = Field(default_factory=list)
    exchange_scope: AttestationExchangeScopeRecord
    validity_window: RegistryFreshnessRecord
    caveat_refs: List[ExchangeCaveatRecord] = Field(default_factory=list)
    proof_refs: List[str] = Field(default_factory=list)
    exchange_status: str  # prepared, validated, exchanged_review_only, exchanged_caveated, exchanged_blocked, exchanged_expired, exchanged_superseded
    warnings: List[str] = Field(default_factory=list)


class AttestationExchangeEnvelopeRecord(BaseModel):
    envelope_id: str
    packet_ref: str
    transmission_time: datetime


class ContinuityAttestationExchangeRecord(BaseModel):
    exchange_id: str
    packet_refs: List[str] = Field(default_factory=list)


class AttestationExchangeManifestRecord(BaseModel):
    manifest_id: str
    generated_at: datetime
    total_exchanges: int


# -----------------------------------------------------------------------------
# TREATY BENCHMARK BASELINE CONTRACTS
# -----------------------------------------------------------------------------


class BenchmarkDimensionRecord(BaseModel):
    dimension_name: (
        str  # treaty_freshness, renewal_timeliness, corridor_scope_clarity, etc.
    )
    description: str
    weight: float = 1.0


class BenchmarkBaselineVersionRecord(BaseModel):
    version_id: str
    semantic_version: EntrySemanticVersionRecord


class BenchmarkDeviationRecord(BaseModel):
    deviation_type: str  # stronger_than_baseline, aligned_with_baseline, narrower_than_baseline, weaker_than_baseline, missing_dimension, stale_baseline_comparison, noncomparable_dimension
    dimension_ref: str
    description: str


class BenchmarkCaveatRecord(BaseModel):
    caveat_code: str
    description: str


class BenchmarkComparisonRecord(BaseModel):
    comparison_id: str
    target_treaty_ref: str
    baseline_ref: str
    deviations: List[BenchmarkDeviationRecord] = Field(default_factory=list)
    caveats: List[BenchmarkCaveatRecord] = Field(default_factory=list)
    computed_at: datetime


class BenchmarkScopeRecord(BaseModel):
    scope_id: str
    applicable_regions: List[str] = Field(default_factory=list)


class BenchmarkDecisionRecord(BaseModel):
    decision: str
    reason: str


class BenchmarkTrendRecord(BaseModel):
    trend_type: str  # baseline_alignment_improving, baseline_alignment_stable, baseline_alignment_degrading, missing_baseline_coverage, stale_baseline_dependency
    description: str


class TreatyBenchmarkBaselineRecord(BaseModel):
    baseline_id: str
    baseline_family: (
        str  # treaty_freshness_baseline, corridor_continuity_baseline, etc.
    )
    baseline_name: str
    applicable_treaty_families: List[str] = Field(default_factory=list)
    dimension_refs: List[BenchmarkDimensionRecord] = Field(default_factory=list)
    version_ref: BenchmarkBaselineVersionRecord
    freshness_state: RegistryFreshnessRecord
    intended_use_scope: str
    warnings: List[str] = Field(default_factory=list)


class BenchmarkManifestRecord(BaseModel):
    manifest_id: str
    generated_at: datetime
    total_comparisons: int


# -----------------------------------------------------------------------------
# POLICY CONFORMANCE PACK CONTRACTS
# -----------------------------------------------------------------------------


class ConformancePackScopeRecord(BaseModel):
    scope_name: str


class ConformancePackDimensionRecord(BaseModel):
    dimension_name: str  # current_treaty_required, current_corridor_required, translation_ledger_required, etc.
    is_required: bool


class ConformancePackEvidenceRecord(BaseModel):
    evidence_id: str
    evidence_type: str
    reference_uri: str


class ConformancePackDecisionRecord(BaseModel):
    decision: str
    reason: str


class ConformancePackGapRecord(BaseModel):
    gap_type: str  # missing_current_treaty, missing_current_corridor, missing_attestation, expired_attestation, etc.
    dimension_ref: str
    is_blocking: bool
    description: str


class ConformancePackValidityRecord(BaseModel):
    valid_from: datetime
    valid_until: datetime


class ConformancePackSupersessionRecord(BaseModel):
    superseded_by_ref: str
    superseded_at: datetime


class SovereignPolicyConformancePackRecord(BaseModel):
    conformance_pack_id: str
    target_scope_ref: str
    region_pair_ref: Optional[str] = None
    corridor_refs: List[str] = Field(default_factory=list)
    treaty_refs: List[str] = Field(default_factory=list)
    required_dimensions: List[ConformancePackDimensionRecord] = Field(
        default_factory=list
    )
    satisfied_dimensions: List[str] = Field(default_factory=list)
    missing_dimensions: List[str] = Field(default_factory=list)
    blocking_gaps: List[ConformancePackGapRecord] = Field(default_factory=list)
    conformance_status: str  # conformant, conformant_with_caveats, review_required, nonconformant, expired, superseded, blocked_by_gap
    evidence_refs: List[ConformancePackEvidenceRecord] = Field(default_factory=list)
    validity_window: ConformancePackValidityRecord
    warnings: List[str] = Field(default_factory=list)


class ConformancePackManifestRecord(BaseModel):
    manifest_id: str
    generated_at: datetime
    total_packs: int
