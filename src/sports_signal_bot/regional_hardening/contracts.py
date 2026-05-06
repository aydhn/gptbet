from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

# --- Enums ---
class RegionalFailoverDrillFamily(str, Enum):
    primary_to_secondary_failover_drill = "primary_to_secondary_failover_drill"
    degraded_regional_failover_drill = "degraded_regional_failover_drill"
    archive_backed_failover_drill = "archive_backed_failover_drill"
    trace_context_failover_drill = "trace_context_failover_drill"
    assurance_surface_failover_drill = "assurance_surface_failover_drill"
    review_surface_failover_drill = "review_surface_failover_drill"
    mixed_regional_failover_drill = "mixed_regional_failover_drill"

class RegionalFailoverStatus(str, Enum):
    failover_ready = "failover_ready"
    failover_caveated = "failover_caveated"
    failover_review_only = "failover_review_only"
    failover_gapped = "failover_gapped"
    failover_blocked = "failover_blocked"
    failover_overclaimed = "failover_overclaimed"

class MultiWaveCutoverRehearsalFamily(str, Enum):
    two_wave_cutover_rehearsal = "two_wave_cutover_rehearsal"
    three_wave_cutover_rehearsal = "three_wave_cutover_rehearsal"
    archive_first_cutover_rehearsal = "archive_first_cutover_rehearsal"
    review_surface_cutover_rehearsal = "review_surface_cutover_rehearsal"
    context_assurance_cutover_rehearsal = "context_assurance_cutover_rehearsal"
    regional_visibility_cutover_rehearsal = "regional_visibility_cutover_rehearsal"
    mixed_surface_cutover_rehearsal = "mixed_surface_cutover_rehearsal"

class CutoverRehearsalStatus(str, Enum):
    cutover_rehearsed_honestly = "cutover_rehearsed_honestly"
    cutover_rehearsed_with_caveats = "cutover_rehearsed_with_caveats"
    review_only_cutover = "review_only_cutover"
    blocked_cutover = "blocked_cutover"
    overclaimed_cutover = "overclaimed_cutover"
    rehearsal_failed = "rehearsal_failed"

class ArchiveMigrationValidationFamily(str, Enum):
    archive_relocation_validation = "archive_relocation_validation"
    archive_split_merge_validation = "archive_split_merge_validation"
    archive_retention_transition_validation = "archive_retention_transition_validation"
    archive_restore_chain_validation = "archive_restore_chain_validation"
    archive_context_assurance_validation = "archive_context_assurance_validation"
    mixed_archive_migration_validation = "mixed_archive_migration_validation"

class ArchiveMigrationValidationStatus(str, Enum):
    migration_validated = "migration_validated"
    migration_validated_with_caveats = "migration_validated_with_caveats"
    review_only_migration = "review_only_migration"
    migration_gapped = "migration_gapped"
    migration_corrupted = "migration_corrupted"
    migration_blocked = "migration_blocked"

class LiveFireVisibilityExerciseFamily(str, Enum):
    no_safe_live_fire_exercise = "no_safe_live_fire_exercise"
    sovereignty_visibility_live_fire_exercise = "sovereignty_visibility_live_fire_exercise"
    degraded_lane_live_fire_exercise = "degraded_lane_live_fire_exercise"
    archive_visibility_live_fire_exercise = "archive_visibility_live_fire_exercise"
    executive_summary_live_fire_exercise = "executive_summary_live_fire_exercise"
    mixed_failure_live_fire_exercise = "mixed_failure_live_fire_exercise"
    cross_region_visibility_live_fire_exercise = "cross_region_visibility_live_fire_exercise"
    continuity_visibility_live_fire_exercise = "continuity_visibility_live_fire_exercise"

class LiveFireVisibilityExerciseStatus(str, Enum):
    visibility_preserved = "visibility_preserved"
    visibility_caveated = "visibility_caveated"
    visibility_review_only = "visibility_review_only"
    visibility_lost = "visibility_lost"
    visibility_overclaimed = "visibility_overclaimed"
    exercise_blocked = "exercise_blocked"

class FailoverCheckpointFamily(str, Enum):
    source_freshness_verified_checkpoint = "source_freshness_verified_checkpoint"
    target_integrity_verified_checkpoint = "target_integrity_verified_checkpoint"
    cross_region_lag_assessed_checkpoint = "cross_region_lag_assessed_checkpoint"
    no_safe_visibility_verified_checkpoint = "no_safe_visibility_verified_checkpoint"
    sovereignty_visibility_verified_checkpoint = "sovereignty_visibility_verified_checkpoint"
    rollback_path_verified_checkpoint = "rollback_path_verified_checkpoint"
    residue_recorded_checkpoint = "residue_recorded_checkpoint"
    failover_honesty_verified_checkpoint = "failover_honesty_verified_checkpoint"

class CutoverWaveFamily(str, Enum):
    pilot_wave = "pilot_wave"
    partial_surface_wave = "partial_surface_wave"
    archive_link_wave = "archive_link_wave"
    full_context_wave = "full_context_wave"
    assurance_surface_wave = "assurance_surface_wave"
    review_surface_wave = "review_surface_wave"
    validation_wave = "validation_wave"
    rollback_validation_wave = "rollback_validation_wave"

class ArchiveRelocationCheckpointFamily(str, Enum):
    source_hash_verified_checkpoint = "source_hash_verified_checkpoint"
    target_hash_verified_checkpoint = "target_hash_verified_checkpoint"
    lineage_preserved_checkpoint = "lineage_preserved_checkpoint"
    replay_support_verified_checkpoint = "replay_support_verified_checkpoint"
    no_safe_visibility_preserved_checkpoint = "no_safe_visibility_preserved_checkpoint"
    sovereignty_note_preserved_checkpoint = "sovereignty_note_preserved_checkpoint"
    migration_residue_recorded_checkpoint = "migration_residue_recorded_checkpoint"
    relocation_honesty_verified_checkpoint = "relocation_honesty_verified_checkpoint"

class LiveFireVisibilityFamily(str, Enum):
    no_safe_marker_visibility = "no_safe_marker_visibility"
    sovereignty_note_visibility = "sovereignty_note_visibility"
    caveat_visibility = "caveat_visibility"
    degraded_lane_visibility = "degraded_lane_visibility"
    residue_visibility = "residue_visibility"
    stale_risk_visibility = "stale_risk_visibility"
    archive_continuity_visibility = "archive_continuity_visibility"
    handoff_visibility = "handoff_visibility"
    region_lag_visibility = "region_lag_visibility"

# --- Models ---

class FailoverRegionRecord(BaseModel):
    region_id: str
    region_type: str
    status: str

class FailoverSourceRecord(FailoverRegionRecord):
    freshness_marker: str

class FailoverTargetRecord(FailoverRegionRecord):
    readiness_marker: str

class FailoverCheckpointRecord(BaseModel):
    checkpoint_id: str
    family: FailoverCheckpointFamily
    status: str

class FailoverLagRecord(BaseModel):
    lag_id: str
    duration_ms: int
    is_visible: bool

class FailoverRollbackRecord(BaseModel):
    rollback_id: str
    readiness: bool

class FailoverResidueRecord(BaseModel):
    residue_id: str
    is_hidden: bool

class RegionalFailoverWarningRecord(BaseModel):
    warning_id: str
    message: str

class RegionalFailoverDrillRecord(BaseModel):
    failover_drill_id: str
    drill_family: RegionalFailoverDrillFamily
    source_region_ref: FailoverSourceRecord
    target_region_ref: FailoverTargetRecord
    checkpoint_refs: List[FailoverCheckpointRecord]
    lag_refs: List[FailoverLagRecord]
    rollback_refs: List[FailoverRollbackRecord]
    residue_refs: List[FailoverResidueRecord]
    failover_status: RegionalFailoverStatus
    warnings: List[RegionalFailoverWarningRecord]

class CutoverWaveRecord(BaseModel):
    wave_id: str
    family: CutoverWaveFamily
    owner: str

class CutoverWindowRecord(BaseModel):
    window_id: str
    duration_ms: int

class CutoverCheckpointRecord(BaseModel):
    checkpoint_id: str
    status: str

class CutoverRollbackRecord(BaseModel):
    rollback_id: str
    path_explicit: bool

class CutoverResidueRecord(BaseModel):
    residue_id: str
    is_visible: bool

class CutoverDecisionRecord(BaseModel):
    decision_id: str
    is_complete: bool

class CutoverWarningRecord(BaseModel):
    warning_id: str
    message: str

class MultiWaveCutoverRehearsalRecord(BaseModel):
    cutover_rehearsal_id: str
    rehearsal_family: MultiWaveCutoverRehearsalFamily
    wave_refs: List[CutoverWaveRecord]
    window_refs: List[CutoverWindowRecord]
    checkpoint_refs: List[CutoverCheckpointRecord]
    rollback_refs: List[CutoverRollbackRecord]
    residue_refs: List[CutoverResidueRecord]
    rehearsal_status: CutoverRehearsalStatus
    warnings: List[CutoverWarningRecord]

class ArchiveMigrationSourceRecord(BaseModel):
    source_id: str
    is_stale: bool

class ArchiveMigrationTargetRecord(BaseModel):
    target_id: str

class ArchiveMigrationSegmentRecord(BaseModel):
    segment_id: str
    is_missing: bool

class ArchiveMigrationHashRecord(BaseModel):
    hash_id: str
    is_continuous: bool

class ArchiveMigrationLineageRecord(BaseModel):
    lineage_id: str
    is_preserved: bool

class ArchiveMigrationReplayRecord(BaseModel):
    replay_id: str
    is_verified: bool

class ArchiveMigrationGapRecord(BaseModel):
    gap_id: str

class ArchiveMigrationWarningRecord(BaseModel):
    warning_id: str
    message: str

class ArchiveMigrationValidationRecord(BaseModel):
    archive_migration_validation_id: str
    validation_family: ArchiveMigrationValidationFamily
    source_archive_ref: ArchiveMigrationSourceRecord
    target_archive_ref: ArchiveMigrationTargetRecord
    segment_refs: List[ArchiveMigrationSegmentRecord]
    hash_refs: List[ArchiveMigrationHashRecord]
    lineage_refs: List[ArchiveMigrationLineageRecord]
    replay_refs: List[ArchiveMigrationReplayRecord]
    gap_refs: List[ArchiveMigrationGapRecord]
    validation_status: ArchiveMigrationValidationStatus
    warnings: List[ArchiveMigrationWarningRecord]

class LiveFireScenarioRecord(BaseModel):
    scenario_id: str

class LiveFireSignalRecord(BaseModel):
    signal_id: str
    is_lost: bool

class LiveFireSurfaceRecord(BaseModel):
    surface_id: str
    family: LiveFireVisibilityFamily
    has_replayable_summary: bool

class LiveFireDecisionRecord(BaseModel):
    decision_id: str

class LiveFireLossRecord(BaseModel):
    loss_id: str
    is_hidden: bool
    is_high_severity: bool

class LiveFireRecoveryRecord(BaseModel):
    recovery_id: str
    has_explicit_marker: bool

class LiveFireWarningRecord(BaseModel):
    warning_id: str
    message: str

class LiveFireVisibilityExerciseRecord(BaseModel):
    live_fire_exercise_id: str
    exercise_family: LiveFireVisibilityExerciseFamily
    scenario_refs: List[LiveFireScenarioRecord]
    signal_refs: List[LiveFireSignalRecord]
    surface_refs: List[LiveFireSurfaceRecord]
    decision_refs: List[LiveFireDecisionRecord]
    loss_refs: List[LiveFireLossRecord]
    recovery_refs: List[LiveFireRecoveryRecord]
    exercise_status: LiveFireVisibilityExerciseStatus
    warnings: List[LiveFireWarningRecord]

class FailoverDependencyRecord(BaseModel):
    pass
class FailoverVerificationRecord(BaseModel):
    pass
class FailoverGapRecord(BaseModel):
    pass
class FailoverContinuityRecord(BaseModel):
    pass
class FailoverLagWindowRecord(BaseModel):
    pass
class FailoverHealthMarkerRecord(BaseModel):
    pass
class RegionalFailoverHealthRecord(BaseModel):
    pass
class RegionalFailoverManifestRecord(BaseModel):
    pass

class CutoverWaveHealthRecord(BaseModel):
    pass
class CutoverManifestRecord(BaseModel):
    pass
class CutoverScopeRecord(BaseModel):
    pass
class CutoverHandoffRecord(BaseModel):
    is_missing: bool
class CutoverLagRecord(BaseModel):
    pass
class CutoverMismatchRecord(BaseModel):
    pass
class CutoverRollbackStepRecord(BaseModel):
    pass
class CutoverRollbackReadinessRecord(BaseModel):
    pass
class CutoverWaveWarningRecord(BaseModel):
    pass

class ArchiveMigrationHealthRecord(BaseModel):
    pass
class ArchiveMigrationManifestRecord(BaseModel):
    pass
class ArchiveRelocationStepRecord(BaseModel):
    pass
class ArchiveChainDependencyRecord(BaseModel):
    pass
class ArchiveRestoreParityRecord(BaseModel):
    pass
class ArchiveRelocationResidueRecord(BaseModel):
    pass
class ArchiveRelocationDriftRecord(BaseModel):
    pass
class ArchiveRelocationHealthMarkerRecord(BaseModel):
    pass

class LiveFireHealthRecord(BaseModel):
    pass
class LiveFireManifestRecord(BaseModel):
    pass
class LiveFireMarkerRecord(BaseModel):
    pass
class LiveFireSuppressionRecord(BaseModel):
    pass
class LiveFireRecoveryStepRecord(BaseModel):
    pass
class LiveFireGapRecord(BaseModel):
    pass
class LiveFireSeverityRecord(BaseModel):
    pass
class LiveFireSurfaceHealthRecord(BaseModel):
    pass
class LiveFireSurfaceWarningRecord(BaseModel):
    pass

class RegionalFailoverBudgetRecord(BaseModel):
    pass
class CutoverBudgetRecord(BaseModel):
    pass
class ArchiveMigrationBudgetRecord(BaseModel):
    pass
class LiveFireVisibilityBudgetRecord(BaseModel):
    pass
class BudgetConsumptionRecord(BaseModel):
    pass
class BudgetBreachRecord(BaseModel):
    pass
class RegionalResilienceBudgetHealthRecord(BaseModel):
    pass
class RegionalResilienceBudgetManifestRecord(BaseModel):
    pass
class RegionalResilienceBudgetWarningRecord(BaseModel):
    pass
