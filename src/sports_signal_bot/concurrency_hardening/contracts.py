import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ConcurrencyGuardConfig(BaseModel):
    guard_family: str
    protected_surface_ref: str
    scope_bounds: Dict[str, Any]
    owner: str
    ordering_rules: Dict[str, Any]
    timeout_ms: int
    cancellation_policy: str


class ConcurrencyGuardWarningRecord(BaseModel):
    warning_id: str
    message: str
    severity: str
    context: Dict[str, Any] = Field(default_factory=dict)


class ConcurrencyGuardRecord(BaseModel):
    concurrency_guard_id: str
    guard_family: str
    protected_surface_ref: str
    guard_scope_ref: str
    ownership_ref: str
    ordering_ref: str
    timeout_ref: str
    cancellation_ref: str
    guard_status: str
    warnings: List[ConcurrencyGuardWarningRecord] = Field(default_factory=list)


class GuardDomainRecord(BaseModel):
    domain_id: str
    description: str


class GuardScopeRecord(BaseModel):
    scope_id: str
    bounds: Dict[str, Any]


class GuardOwnershipRecord(BaseModel):
    ownership_id: str
    owner: str


class GuardOrderingRecord(BaseModel):
    ordering_id: str
    rules: Dict[str, Any]


class GuardJoinRecord(BaseModel):
    join_id: str
    policy: str


class GuardCancellationRecord(BaseModel):
    cancellation_id: str
    policy: str


class GuardTimeoutRecord(BaseModel):
    timeout_id: str
    duration_ms: int


class ConcurrencyGuardHealthRecord(BaseModel):
    health_id: str
    is_healthy: bool
    status_summary: str
    failing_guards: List[str]


class ConcurrencyGuardManifestRecord(BaseModel):
    manifest_id: str
    generated_at: datetime.datetime
    guards: List[ConcurrencyGuardRecord]
    health: ConcurrencyGuardHealthRecord


# Bounded Parallelism
class ParallelismWarningRecord(BaseModel):
    warning_id: str
    message: str
    severity: str
    context: Dict[str, Any] = Field(default_factory=dict)


class ParallelExecutionPlanRecord(BaseModel):
    parallel_plan_id: str
    plan_family: str
    lane_refs: List[str]
    worker_pool_refs: List[str]
    queue_budget_refs: List[str]
    join_refs: List[str]
    max_parallelism: int
    backpressure_policy_ref: str
    plan_status: str
    warnings: List[ParallelismWarningRecord] = Field(default_factory=list)


class ParallelLaneRecord(BaseModel):
    lane_id: str
    capacity: int


class WorkerPoolRecord(BaseModel):
    pool_id: str
    size: int


class QueueBudgetRecord(BaseModel):
    budget_id: str
    max_items: int


class BackpressureRecord(BaseModel):
    policy_id: str
    action: str


class ParallelJoinRecord(BaseModel):
    join_id: str
    strategy: str


class ParallelResultRecord(BaseModel):
    result_id: str
    plan_ref: str
    success: bool


class ParallelDeviationRecord(BaseModel):
    deviation_id: str
    description: str


class ParallelismHealthRecord(BaseModel):
    health_id: str
    is_healthy: bool
    status_summary: str


class ParallelismManifestRecord(BaseModel):
    manifest_id: str
    generated_at: datetime.datetime
    plans: List[ParallelExecutionPlanRecord]
    health: ParallelismHealthRecord


# Async Ordering
class OrderingWarningRecord(BaseModel):
    warning_id: str
    message: str
    severity: str
    context: Dict[str, Any] = Field(default_factory=dict)


class AsyncOrderingRecord(BaseModel):
    ordering_id: str
    target_ref: str
    rules: Dict[str, Any]
    status: str
    warnings: List[OrderingWarningRecord] = Field(default_factory=list)


class OrderingDependencyRecord(BaseModel):
    dependency_id: str
    requires: str


class OrderingBarrierRecord(BaseModel):
    barrier_id: str
    wait_for: List[str]


class OrderingViolationRecord(BaseModel):
    violation_id: str
    description: str


class OrderingRecoveryRecord(BaseModel):
    recovery_id: str
    action: str


class OrderingParityRecord(BaseModel):
    parity_id: str
    match: bool


class OrderingHealthRecord(BaseModel):
    health_id: str
    is_healthy: bool
    status_summary: str


class OrderingManifestRecord(BaseModel):
    manifest_id: str
    generated_at: datetime.datetime
    orderings: List[AsyncOrderingRecord]
    health: OrderingHealthRecord


# Race Probes
class RaceProbeWarningRecord(BaseModel):
    warning_id: str
    message: str
    severity: str
    context: Dict[str, Any] = Field(default_factory=dict)


class RaceProbeRunRecord(BaseModel):
    run_id: str
    scenario_ref: str
    schedule_ref: str
    run_status: str
    violations_detected: int
    warnings: List[RaceProbeWarningRecord] = Field(default_factory=list)


class RaceProbeScenarioRecord(BaseModel):
    scenario_id: str
    family: str


class RaceProbeScheduleRecord(BaseModel):
    schedule_id: str
    seed: int
    perturbation: str


class RaceProbeSignalRecord(BaseModel):
    signal_id: str
    type: str


class RaceProbeViolationRecord(BaseModel):
    violation_id: str
    description: str


class RaceProbeClusterRecord(BaseModel):
    cluster_id: str
    violations: List[str]


class RaceProbeRecoveryRecord(BaseModel):
    recovery_id: str
    action: str


class RaceProbeHealthRecord(BaseModel):
    health_id: str
    is_healthy: bool
    status_summary: str


class RaceProbeManifestRecord(BaseModel):
    manifest_id: str
    generated_at: datetime.datetime
    runs: List[RaceProbeRunRecord]
    health: RaceProbeHealthRecord


# Shared State
class SharedStateWarningRecord(BaseModel):
    warning_id: str
    message: str
    severity: str
    context: Dict[str, Any] = Field(default_factory=dict)


class SharedStateRecord(BaseModel):
    state_id: str
    owner_ref: str
    surface_desc: str
    status: str
    warnings: List[SharedStateWarningRecord] = Field(default_factory=list)


class StateOwnerRecord(BaseModel):
    owner_id: str
    identity: str


class StateMutationRecord(BaseModel):
    mutation_id: str
    state_ref: str


class StateAccessRecord(BaseModel):
    access_id: str
    state_ref: str


class StateConflictRecord(BaseModel):
    conflict_id: str
    description: str


class StateVersionRecord(BaseModel):
    version_id: str
    version: int


class SharedStateHealthRecord(BaseModel):
    health_id: str
    is_healthy: bool
    status_summary: str


class SharedStateManifestRecord(BaseModel):
    manifest_id: str
    generated_at: datetime.datetime
    states: List[SharedStateRecord]
    health: SharedStateHealthRecord


# Idempotency
class IdempotencyWarningRecord(BaseModel):
    warning_id: str
    message: str
    severity: str
    context: Dict[str, Any] = Field(default_factory=dict)


class IdempotencyRecord(BaseModel):
    idempotency_id: str
    target_ref: str
    key_ref: str
    status: str
    warnings: List[IdempotencyWarningRecord] = Field(default_factory=list)


class IdempotencyKeyRecord(BaseModel):
    key_id: str
    value: str


class SideEffectRecord(BaseModel):
    effect_id: str
    description: str


class SideEffectReplayRecord(BaseModel):
    replay_id: str
    effect_ref: str


class DuplicateExecutionRecord(BaseModel):
    duplicate_id: str
    description: str


class IdempotencyHealthRecord(BaseModel):
    health_id: str
    is_healthy: bool
    status_summary: str


class IdempotencyManifestRecord(BaseModel):
    manifest_id: str
    generated_at: datetime.datetime
    records: List[IdempotencyRecord]
    health: IdempotencyHealthRecord


# Stale Reads
class DriftWarningRecord(BaseModel):
    warning_id: str
    message: str
    severity: str
    context: Dict[str, Any] = Field(default_factory=dict)


class StaleReadRecord(BaseModel):
    stale_read_id: str
    target_ref: str
    drift_window_ref: str
    status: str
    warnings: List[DriftWarningRecord] = Field(default_factory=list)


class FreshnessSnapshotRecord(BaseModel):
    snapshot_id: str
    timestamp: datetime.datetime


class DriftWindowRecord(BaseModel):
    window_id: str
    max_drift_ms: int


class DriftViolationRecord(BaseModel):
    violation_id: str
    drift_ms: int


class DriftCompensationRecord(BaseModel):
    compensation_id: str
    action: str


class DriftHealthRecord(BaseModel):
    health_id: str
    is_healthy: bool
    status_summary: str


class DriftManifestRecord(BaseModel):
    manifest_id: str
    generated_at: datetime.datetime
    records: List[StaleReadRecord]
    health: DriftHealthRecord


# Queues
class QueueWarningRecord(BaseModel):
    warning_id: str
    message: str
    severity: str
    context: Dict[str, Any] = Field(default_factory=dict)


class QueueDisciplineRecord(BaseModel):
    discipline_id: str
    target_queue: str
    status: str
    warnings: List[QueueWarningRecord] = Field(default_factory=list)


class QueueSampleRecord(BaseModel):
    sample_id: str
    length: int


class QueueOverflowRecord(BaseModel):
    overflow_id: str
    dropped_items: int


class QueueDrainRecord(BaseModel):
    drain_id: str
    duration_ms: int


class BackpressureDecisionRecord(BaseModel):
    decision_id: str
    action: str


class QueueHealthRecord(BaseModel):
    health_id: str
    is_healthy: bool
    status_summary: str


class QueueManifestRecord(BaseModel):
    manifest_id: str
    generated_at: datetime.datetime
    disciplines: List[QueueDisciplineRecord]
    health: QueueHealthRecord


# Timeout/Cancellation
class TimeoutWarningRecord(BaseModel):
    warning_id: str
    message: str
    severity: str
    context: Dict[str, Any] = Field(default_factory=dict)


class CancellationRunRecord(BaseModel):
    run_id: str
    target_ref: str
    status: str
    warnings: List[TimeoutWarningRecord] = Field(default_factory=list)


class TimeoutRunRecord(BaseModel):
    run_id: str
    target_ref: str
    status: str
    warnings: List[TimeoutWarningRecord] = Field(default_factory=list)


class PartialCompletionRecord(BaseModel):
    partial_id: str
    description: str


class CleanupRecord(BaseModel):
    cleanup_id: str
    action: str


class CancellationLeakRecord(BaseModel):
    leak_id: str
    description: str


class TimeoutCompensationRecord(BaseModel):
    compensation_id: str
    action: str


class CancellationHealthRecord(BaseModel):
    health_id: str
    is_healthy: bool
    status_summary: str


class TimeoutManifestRecord(BaseModel):
    manifest_id: str
    generated_at: datetime.datetime
    runs: List[TimeoutRunRecord]
    health: CancellationHealthRecord


# Regressions
class ConcurrencyRegressionWarningRecord(BaseModel):
    warning_id: str
    message: str
    severity: str
    context: Dict[str, Any] = Field(default_factory=dict)


class ConcurrencyRegressionRecord(BaseModel):
    regression_id: str
    baseline_ref: str
    comparison_ref: str
    impact_ref: str
    severity_ref: str
    status: str
    warnings: List[ConcurrencyRegressionWarningRecord] = Field(default_factory=list)


class ConcurrencyBaselineRecord(BaseModel):
    baseline_id: str
    metrics: Dict[str, float]


class ConcurrencyComparisonRecord(BaseModel):
    comparison_id: str
    metrics: Dict[str, float]


class ConcurrencyImpactRecord(BaseModel):
    impact_id: str
    description: str


class ConcurrencySeverityRecord(BaseModel):
    severity_id: str
    level: str


class ConcurrencyRegressionHealthRecord(BaseModel):
    health_id: str
    is_healthy: bool
    status_summary: str


class ConcurrencyRegressionManifestRecord(BaseModel):
    manifest_id: str
    generated_at: datetime.datetime
    regressions: List[ConcurrencyRegressionRecord]
    health: ConcurrencyRegressionHealthRecord
