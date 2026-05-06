from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

# --- SOAK ENDURANCE CONTRACTS ---

class SoakScenarioRecord(BaseModel):
    scenario_id: str
    scenario_family: str

class SoakWindowRecord(BaseModel):
    start_time: str
    end_time: str
    elapsed_runtime: str

class SoakCycleRecord(BaseModel):
    cycle_id: str
    cycle_index: int
    cycle_outcome: str

class SoakResourceRecord(BaseModel):
    resource_id: str
    metrics: Dict[str, Any]

class SoakResidueRecord(BaseModel):
    residue_id: str
    amount: float

class SoakDeviationRecord(BaseModel):
    deviation_id: str
    severity: str

class SoakOutcomeRecord(BaseModel):
    outcome_status: str

class SoakHealthRecord(BaseModel):
    health_status: str

class SoakManifestRecord(BaseModel):
    manifest_id: str
    version: str

class SoakWarningRecord(BaseModel):
    warning_id: str
    message: str

class SoakEnduranceRunRecord(BaseModel):
    soak_run_id: str
    run_family: str
    scenario_refs: List[str]
    cycle_count: int
    elapsed_runtime_window: str
    seed_ref: str
    environment_hash: str
    aggregate_latency_stats: Dict[str, float]
    aggregate_memory_stats: Dict[str, float]
    aggregate_queue_stats: Dict[str, float]
    aggregate_residue_stats: Dict[str, float]
    outcome_status: str
    warnings: List[str] = Field(default_factory=list)


# --- LONG-HORIZON DRIFT DETECTION CONTRACTS ---

class DriftBaselineRecord(BaseModel):
    baseline_id: str
    metrics: Dict[str, float]

class DriftSampleRecord(BaseModel):
    sample_id: str
    timestamp: str

class DriftMetricRecord(BaseModel):
    metric_name: str
    value: float

class DriftClusterRecord(BaseModel):
    cluster_id: str

class DriftThresholdRecord(BaseModel):
    metric_name: str
    max_drift: float

class DriftViolationRecord(BaseModel):
    violation_id: str
    metric: str
    severity: str

class DriftTrendRecord(BaseModel):
    metric: str
    trend_direction: str

class DriftHealthRecord(BaseModel):
    health_status: str

class DriftManifestRecord(BaseModel):
    manifest_id: str

class DriftWarningRecord(BaseModel):
    warning_id: str
    message: str

class DriftDetectionRunRecord(BaseModel):
    drift_run_id: str
    baselines: List[DriftBaselineRecord]
    violations: List[DriftViolationRecord]
    status: str


# --- ARCHIVAL INTEGRITY CONTRACTS ---

class ArchiveSegmentRecord(BaseModel):
    segment_id: str

class ArchiveHashRecord(BaseModel):
    hash_value: str

class ArchiveCompletenessRecord(BaseModel):
    status: str

class ArchiveLineageRecord(BaseModel):
    lineage_id: str

class ArchiveReplaySupportRecord(BaseModel):
    supported: bool

class ArchiveRestorationCheckRecord(BaseModel):
    check_id: str
    passed: bool

class ArchivalHealthRecord(BaseModel):
    health_status: str

class ArchivalManifestRecord(BaseModel):
    manifest_id: str

class ArchivalWarningRecord(BaseModel):
    warning_id: str
    message: str

class ArchiveSnapshotRecord(BaseModel):
    archive_snapshot_id: str
    snapshot_family: str
    source_run_ref: str
    source_manifest_ref: str
    artifact_refs: List[str]
    hash_refs: List[str]
    lineage_refs: List[str]
    completeness_status: str
    replay_support_status: str
    warnings: List[str] = Field(default_factory=list)

class ArchivalIntegrityRunRecord(BaseModel):
    integrity_run_id: str
    snapshots: List[ArchiveSnapshotRecord]


# --- ARCHIVE REPLAY / RESTORE CONTRACTS ---

class ArchiveReplayRecord(BaseModel):
    replay_id: str

class RestoreDiffRecord(BaseModel):
    diff_id: str

class RestoreDeviationRecord(BaseModel):
    deviation_id: str

class RestoreHealthRecord(BaseModel):
    health_status: str

class RestoreManifestRecord(BaseModel):
    manifest_id: str

class RestoreWarningRecord(BaseModel):
    warning_id: str
    message: str

class ArchiveRestoreRecord(BaseModel):
    restore_id: str
    snapshot_ref: str
    status: str


# --- ARCHIVE ROT / RETENTION CONTRACTS ---

class ArchiveRetentionRecord(BaseModel):
    retention_id: str
    policy: str

class ArchiveRotSignalRecord(BaseModel):
    signal_id: str
    severity: str

class ArchiveExpiryRecord(BaseModel):
    expiry_id: str

class ArchiveMigrationRecord(BaseModel):
    migration_id: str

class ArchiveResidueRecord(BaseModel):
    residue_id: str

class ArchiveRetentionHealthRecord(BaseModel):
    health_status: str

class ArchiveRetentionManifestRecord(BaseModel):
    manifest_id: str

class ArchiveRetentionWarningRecord(BaseModel):
    warning_id: str
    message: str


# --- RUNBOOK VERIFICATION CONTRACTS ---

class RunbookStepRecord(BaseModel):
    step_id: str
    action: str

class RunbookExecutionRecord(BaseModel):
    execution_id: str

class RunbookGapRecord(BaseModel):
    gap_id: str
    severity: str

class RunbookDecisionRecord(BaseModel):
    decision_id: str

class RunbookEscalationRecord(BaseModel):
    escalation_id: str

class RunbookCoverageRecord(BaseModel):
    coverage_score: float

class RunbookHealthRecord(BaseModel):
    health_status: str

class RunbookManifestRecord(BaseModel):
    manifest_id: str

class RunbookWarningRecord(BaseModel):
    warning_id: str
    message: str

class RunbookRecord(BaseModel):
    runbook_id: str
    runbook_family: str
    intended_operator_profile: str
    step_refs: List[str]
    escalation_refs: List[str]
    precondition_refs: List[str]
    postcondition_refs: List[str]
    runbook_status: str
    warnings: List[str] = Field(default_factory=list)

class RunbookVerificationRecord(BaseModel):
    verification_id: str
    runbooks: List[RunbookRecord]


# --- RUNBOOK EXECUTION REHEARSALS ---

class RehearsalInputRecord(BaseModel):
    input_id: str

class RehearsalStepExecutionRecord(BaseModel):
    execution_id: str

class RehearsalMismatchRecord(BaseModel):
    mismatch_id: str

class RehearsalCoverageRecord(BaseModel):
    coverage: float

class RehearsalHealthRecord(BaseModel):
    health_status: str

class RehearsalManifestRecord(BaseModel):
    manifest_id: str

class RehearsalWarningRecord(BaseModel):
    warning_id: str
    message: str

class RunbookRehearsalRecord(BaseModel):
    rehearsal_id: str
    runbook_ref: str
    status: str


# --- RESIDUE ACCUMULATION CONTRACTS ---

class ResidueSampleRecord(BaseModel):
    sample_id: str

class ResidueTrendRecord(BaseModel):
    trend_id: str
    direction: str

class ResidueThresholdRecord(BaseModel):
    threshold_id: str

class ResidueViolationRecord(BaseModel):
    violation_id: str

class ResidueHealthRecord(BaseModel):
    health_status: str

class ResidueManifestRecord(BaseModel):
    manifest_id: str

class ResidueWarningRecord(BaseModel):
    warning_id: str

class ResidueAccumulationRecord(BaseModel):
    accumulation_id: str
    trends: List[ResidueTrendRecord]
    violations: List[ResidueViolationRecord]


# --- ENDURANCE BUDGETS ---

class DriftBudgetRecord(BaseModel):
    budget_id: str

class ArchiveBudgetRecord(BaseModel):
    budget_id: str

class RunbookBudgetRecord(BaseModel):
    budget_id: str

class EnduranceBudgetHealthRecord(BaseModel):
    health_status: str

class EnduranceBudgetManifestRecord(BaseModel):
    manifest_id: str

class EnduranceBudgetWarningRecord(BaseModel):
    warning_id: str

class EnduranceBudgetRecord(BaseModel):
    budget_id: str
    status: str


# --- LONG-HORIZON REGRESSION DETECTION ---

class LongHorizonBaselineRecord(BaseModel):
    baseline_id: str

class LongHorizonComparisonRecord(BaseModel):
    comparison_id: str

class LongHorizonImpactRecord(BaseModel):
    impact_id: str

class LongHorizonSeverityRecord(BaseModel):
    severity: str

class LongHorizonHealthRecord(BaseModel):
    health_status: str

class LongHorizonManifestRecord(BaseModel):
    manifest_id: str

class LongHorizonWarningRecord(BaseModel):
    warning_id: str

class LongHorizonRegressionRecord(BaseModel):
    regression_id: str
    severity: str
    impacts: List[LongHorizonImpactRecord]
