from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime

# GEO-DISTRIBUTED FAILOVER MESH CONTRACTS
class GeoFailoverMeshRecord(BaseModel):
    geo_failover_mesh_id: str
    mesh_family: str
    node_refs: List[str]
    edge_refs: List[str]
    path_refs: List[str]
    lag_refs: List[str]
    continuity_refs: List[str]
    residue_refs: List[str]
    mesh_status: str
    warnings: List[str] = Field(default_factory=list)

class GeoMeshNodeRecord(BaseModel):
    node_id: str
    region: str
    is_stale: bool
    freshness_note: str


class GeoMeshEdgeRecord(BaseModel):
    edge_id: str
    source_node: str
    target_node: str
    status: str


class GeoMeshPathRecord(BaseModel):
    path_id: str
    nodes: List[str]
    lag_ms: int


class GeoMeshLagRecord(BaseModel):
    lag_id: str
    source: str
    target: str
    lag_seconds: int


class GeoMeshContinuityRecord(BaseModel):
    continuity_id: str
    is_preserved: bool


class GeoMeshDecisionRecord(BaseModel):
    decision_id: str
    action: str


class GeoMeshResidueRecord(BaseModel):
    residue_id: str
    amount: int


class GeoMeshHealthRecord(BaseModel):
    health_id: str
    status: str


class GeoFailoverMeshManifestRecord(BaseModel):
    manifest_id: str
    version: str


class GeoFailoverMeshWarningRecord(BaseModel):
    warning_id: str
    message: str


# GEO MESH NODE / EDGE MODEL
class GeoNodeFreshnessRecord(BaseModel):
    node_id: str
    last_seen: int


class GeoNodeOwnerRecord(BaseModel):
    node_id: str
    owner: str


class GeoEdgeContinuityRecord(BaseModel):
    edge_id: str
    continuity: str


class GeoEdgeGapRecord(BaseModel):
    edge_id: str
    gap_size: int


class GeoEdgeRollbackRecord(BaseModel):
    edge_id: str
    can_rollback: bool


class GeoMeshHealthMarkerRecord(BaseModel):
    marker_id: str


# ACTIVE-ACTIVE REHEARSAL GOVERNANCE CONTRACTS
class ActiveActiveRehearsalRecord(BaseModel):
    active_active_rehearsal_id: str
    rehearsal_family: str
    region_pair_refs: List[str]
    symmetry_refs: List[str]
    divergence_refs: List[str]
    conflict_refs: List[str]
    fallback_refs: List[str]
    residue_refs: List[str]
    rehearsal_status: str
    warnings: List[str] = Field(default_factory=list)

class RehearsalRegionPairRecord(BaseModel):
    pair_id: str
    region_a: str
    region_b: str


class RehearsalSymmetryRecord(BaseModel):
    symmetry_id: str
    is_symmetric: bool


class RehearsalDivergenceRecord(BaseModel):
    divergence_id: str
    severity: str


class RehearsalConflictRecord(BaseModel):
    conflict_id: str
    resolved: bool


class RehearsalFallbackRecord(BaseModel):
    fallback_id: str
    path: str


class RehearsalResidueRecord(BaseModel):
    residue_id: str
    type: str


class ActiveActiveGovernanceDecisionRecord(BaseModel):
    decision_id: str


class ActiveActiveHealthRecord(BaseModel):
    health_id: str


class ActiveActiveManifestRecord(BaseModel):
    manifest_id: str


class ActiveActiveWarningRecord(BaseModel):
    warning_id: str


# SYMMETRY / DIVERGENCE MODEL
class SymmetryMetricRecord(BaseModel):
    metric_id: str
    value: float


class DivergenceWindowRecord(BaseModel):
    window_id: str
    duration: int


class DivergenceSeverityRecord(BaseModel):
    severity_id: str
    level: str


class ConflictLineageRecord(BaseModel):
    lineage_id: str


class DualWriterRiskRecord(BaseModel):
    risk_id: str
    probability: float


class RehearsalConvergenceRecord(BaseModel):
    convergence_id: str


class RehearsalSymmetryHealthRecord(BaseModel):
    health_id: str


# ARCHIVE RELOCATION WAVE CONTRACTS
class ArchiveRelocationWaveRecord(BaseModel):
    relocation_wave_id: str
    wave_family: str
    stage_refs: List[str]
    segment_refs: List[str]
    hash_refs: List[str]
    lineage_refs: List[str]
    replay_refs: List[str]
    residue_refs: List[str]
    rollback_refs: List[str]
    wave_status: str
    warnings: List[str] = Field(default_factory=list)

class RelocationWaveStageRecord(BaseModel):
    stage_id: str


class RelocationWaveSegmentRecord(BaseModel):
    segment_id: str


class RelocationWaveHashRecord(BaseModel):
    hash_id: str
    hash_value: str


class RelocationWaveLineageRecord(BaseModel):
    lineage_id: str


class RelocationWaveReplayRecord(BaseModel):
    replay_id: str


class RelocationWaveResidueRecord(BaseModel):
    residue_id: str


class RelocationWaveRollbackRecord(BaseModel):
    rollback_id: str


class ArchiveRelocationWaveHealthRecord(BaseModel):
    health_id: str


class ArchiveRelocationWaveManifestRecord(BaseModel):
    manifest_id: str


class ArchiveRelocationWaveWarningRecord(BaseModel):
    warning_id: str


# WAVE STAGE / ROLLBACK MODEL
class RelocationWaveDependencyRecord(BaseModel):
    dep_id: str


class RelocationWaveGapRecord(BaseModel):
    gap_id: str


class RelocationWaveDriftRecord(BaseModel):
    drift_id: str


class RelocationWaveVisibilityRecord(BaseModel):
    visibility_id: str


class RelocationWaveCheckpointRecord(BaseModel):
    checkpoint_id: str


class RelocationWaveHealthMarkerRecord(BaseModel):
    marker_id: str


# MULTI-REGION OPERATOR CALENDAR AUDIT CONTRACTS
class OperatorCalendarAuditRecord(BaseModel):
    operator_calendar_audit_id: str
    audit_family: str
    region_refs: List[str]
    coverage_window_refs: List[str]
    owner_refs: List[str]
    overlap_refs: List[str]
    gap_refs: List[str]
    escalation_reachability_refs: List[str]
    residue_refs: List[str]
    audit_status: str
    warnings: List[str] = Field(default_factory=list)

class CalendarRegionRecord(BaseModel):
    region_id: str


class CalendarCoverageWindowRecord(BaseModel):
    window_id: str


class CalendarOwnerRecord(BaseModel):
    owner_id: str


class CalendarOverlapRecord(BaseModel):
    overlap_id: str


class CalendarGapRecord(BaseModel):
    gap_id: str


class CalendarEscalationReachabilityRecord(BaseModel):
    reach_id: str


class CalendarResidueRecord(BaseModel):
    residue_id: str


class OperatorCalendarHealthRecord(BaseModel):
    health_id: str


class OperatorCalendarManifestRecord(BaseModel):
    manifest_id: str


class OperatorCalendarWarningRecord(BaseModel):
    warning_id: str


# CALENDAR COVERAGE / HANDOFF MODEL
class CalendarShiftRecord(BaseModel):
    shift_id: str


class CalendarHandoffRecord(BaseModel):
    handoff_id: str


class CalendarAckRecord(BaseModel):
    ack_id: str


class CalendarEscalationWindowRecord(BaseModel):
    window_id: str


class CalendarMismatchRecord(BaseModel):
    mismatch_id: str


class CalendarContinuityRecord(BaseModel):
    continuity_id: str


class CalendarHealthMarkerRecord(BaseModel):
    marker_id: str


# GEO RESILIENCE BUDGETS
class GeoFailoverBudgetRecord(BaseModel):
    budget_id: str


class ActiveActiveBudgetRecord(BaseModel):
    budget_id: str


class RelocationWaveBudgetRecord(BaseModel):
    budget_id: str


class CalendarCoverageBudgetRecord(BaseModel):
    budget_id: str


class BudgetConsumptionRecord(BaseModel):
    consumption_id: str


class BudgetBreachRecord(BaseModel):
    breach_id: str


class GeoResilienceBudgetHealthRecord(BaseModel):
    health_id: str


class GeoResilienceBudgetManifestRecord(BaseModel):
    manifest_id: str


class GeoResilienceBudgetWarningRecord(BaseModel):
    warning_id: str
