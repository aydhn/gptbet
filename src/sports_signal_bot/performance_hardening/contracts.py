from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any, Union

# --- Performance Envelope Contracts ---

class PerformanceEnvelopeRecord(BaseModel):
    performance_envelope_id: str
    envelope_family: str
    target_surface_ref: str
    latency_budget_ms: float
    memory_budget_mb: float
    serialization_budget_ms: float
    io_budget_ms: float
    artifact_size_budget_kb: float
    envelope_status: str
    warnings: List[str] = Field(default_factory=list)

class PerformanceBudgetRecord(BaseModel):
    latency_ms: float
    memory_mb: float
    serialization_ms: float
    io_ms: float
    artifact_size_kb: float

class PerformanceMeasurementRecord(BaseModel):
    latency_ms: float
    memory_mb: float
    serialization_ms: float
    io_ms: float
    artifact_size_kb: float

class PerformanceCeilingRecord(BaseModel):
    hard_latency_limit_ms: float
    hard_memory_limit_mb: float

class PerformanceDeviationRecord(BaseModel):
    metric: str
    allowed_value: float
    actual_value: float
    deviation_percentage: float

class PerformanceEnvelopeDecisionRecord(BaseModel):
    decision: str
    reason: str

class PerformanceEnvelopeHealthRecord(BaseModel):
    is_healthy: bool
    status_summary: str
    violation_count: int

class PerformanceEnvelopeManifestRecord(BaseModel):
    timestamp: str
    envelopes: List[PerformanceEnvelopeRecord]

class PerformanceEnvelopeWarningRecord(BaseModel):
    warning_type: str
    message: str

# --- Load Profiling Contracts ---

class LoadProfilingRunRecord(BaseModel):
    load_profiling_run_id: str
    run_family: str
    scenario_refs: List[str]
    sample_count: int
    warmup_count: int
    seed_ref: str
    environment_hash: str
    aggregate_latency_stats: Dict[str, float]
    aggregate_memory_stats: Dict[str, float]
    aggregate_io_stats: Dict[str, float]
    aggregate_variance_stats: Dict[str, float]
    profiling_status: str
    warnings: List[str] = Field(default_factory=list)

class LoadProfileScenarioRecord(BaseModel):
    scenario_id: str
    scenario_family: str
    description: str

class LoadSampleRecord(BaseModel):
    sample_id: str
    latency_ms: float
    memory_mb: float
    io_ms: float

class LoadLatencyRecord(BaseModel):
    min_ms: float
    max_ms: float
    p50_ms: float
    p95_ms: float
    p99_ms: float

class LoadMemoryRecord(BaseModel):
    peak_mb: float
    avg_mb: float

class LoadIORecord(BaseModel):
    read_ms: float
    write_ms: float

class LoadSerializationRecord(BaseModel):
    duration_ms: float
    bytes_produced: int

class LoadVarianceRecord(BaseModel):
    std_dev_latency: float
    variance_memory: float

class LoadProfilingHealthRecord(BaseModel):
    is_stable: bool
    variance_level: str

class LoadProfilingManifestRecord(BaseModel):
    timestamp: str
    runs: List[LoadProfilingRunRecord]

class LoadProfilingWarningRecord(BaseModel):
    warning_type: str
    message: str

# --- Hot-Path Discovery and Simplification Contracts ---

class HotPathRecord(BaseModel):
    hot_path_id: str
    hot_path_family: str
    source_command_ref: str
    dominant_segment_refs: List[str]
    cumulative_latency_ms: float
    cumulative_memory_mb: float
    dominant_cost_family: str
    simplification_candidate_refs: List[str]
    hot_path_status: str
    warnings: List[str] = Field(default_factory=list)

class HotPathSegmentRecord(BaseModel):
    segment_id: str
    function_name: str
    cost_ms: float
    percentage_of_total: float

class HotPathCostRecord(BaseModel):
    cost_family: str
    value: float

class HotPathCallGraphRecord(BaseModel):
    graph_id: str
    nodes: List[str]
    edges: List[Dict[str, str]]

class HotPathSimplificationRecord(BaseModel):
    simplification_id: str
    description: str
    expected_gain_ms: float

class HotPathBeforeAfterRecord(BaseModel):
    before_latency_ms: float
    after_latency_ms: float
    improvement_percentage: float

class HotPathRegressionRecord(BaseModel):
    regression_id: str
    latency_increase_ms: float

class HotPathHealthRecord(BaseModel):
    has_critical_hot_paths: bool

class HotPathManifestRecord(BaseModel):
    timestamp: str
    hot_paths: List[HotPathRecord]

class HotPathWarningRecord(BaseModel):
    warning_type: str
    message: str

# --- Bounded Cache Discipline Contracts ---

class CachePolicyRecord(BaseModel):
    cache_policy_id: str
    cache_family: str
    namespace_ref: str
    ttl_seconds: int
    invalidation_rule_refs: List[str]
    staleness_risk_level: str
    cache_scope: str
    cache_status: str
    warnings: List[str] = Field(default_factory=list)

class CacheNamespaceRecord(BaseModel):
    namespace_id: str
    description: str

class CacheKeyRecord(BaseModel):
    key_hash: str
    deterministic_components: Dict[str, Any]

class CacheEntryRecord(BaseModel):
    key: str
    value_ref: str
    created_at: str
    expires_at: str

class CacheTTLRecord(BaseModel):
    ttl_seconds: int

class CacheInvalidationRecord(BaseModel):
    invalidation_id: str
    trigger_ref: str
    keys_invalidated: List[str]

class CacheFreshnessGuardRecord(BaseModel):
    guard_id: str
    rule: str

class CacheHitMissRecord(BaseModel):
    hits: int
    misses: int
    stale_hits_prevented: int

class CacheDisciplineHealthRecord(BaseModel):
    is_healthy: bool
    stale_risk_detected: bool

class CacheManifestRecord(BaseModel):
    timestamp: str
    policies: List[CachePolicyRecord]

class CacheWarningRecord(BaseModel):
    warning_type: str
    message: str

# --- Cache Invalidation Contracts ---

class CacheInvalidationEventRecord(BaseModel):
    event_id: str
    timestamp: str
    namespace: str
    reason: str

class CacheDependencyRecord(BaseModel):
    source_ref: str
    target_cache_keys: List[str]

class CacheResidueRecord(BaseModel):
    residue_keys: List[str]

class CacheBypassRecord(BaseModel):
    bypass_reason: str
    key: str

class CacheRecomputeRecord(BaseModel):
    key: str
    recompute_time_ms: float

class CacheInvalidationHealthRecord(BaseModel):
    has_unhandled_residue: bool

class CacheInvalidationManifestRecord(BaseModel):
    timestamp: str
    events: List[CacheInvalidationEventRecord]

class CacheInvalidationWarningRecord(BaseModel):
    warning_type: str
    message: str

# --- Performance Regression Detection ---

class PerformanceRegressionRecord(BaseModel):
    regression_id: str
    metric: str
    baseline_value: float
    current_value: float
    severity: str

class RegressionBaselineRecord(BaseModel):
    baseline_id: str
    metrics: Dict[str, float]

class RegressionComparisonRecord(BaseModel):
    metric: str
    difference: float
    percentage: float

class RegressionBudgetImpactRecord(BaseModel):
    budget_exceeded: bool
    excess_amount: float

class RegressionSeverityRecord(BaseModel):
    level: str
    description: str

class RegressionHealthRecord(BaseModel):
    has_release_blockers: bool

class PerformanceRegressionManifestRecord(BaseModel):
    timestamp: str
    regressions: List[PerformanceRegressionRecord]

class PerformanceRegressionWarningRecord(BaseModel):
    warning_type: str
    message: str
