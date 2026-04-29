from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime

class PerformanceProfileRecord(BaseModel):
    run_id: str
    component_name: str
    step_name: str
    started_at: datetime
    ended_at: datetime
    duration_ms: float
    row_count: Optional[int] = None
    byte_size: Optional[int] = None
    cache_status: str
    recompute_mode: str
    warnings: List[str] = Field(default_factory=list)

class StepTimingRecord(BaseModel):
    step_name: str
    duration_ms: float
    started_at: datetime

class CacheEntryRecord(BaseModel):
    cache_family: str
    cache_key: str
    created_at: datetime
    expires_at: Optional[datetime] = None
    freshness_policy: str
    invalidation_triggers: List[str] = Field(default_factory=list)
    payload_reference: str
    hit_count: Optional[int] = 0
    last_accessed_at: datetime
    size_bytes: Optional[int] = None
    producer_version: str

class CacheKeyRecord(BaseModel):
    key: str
    inputs: Dict[str, Any]

class CacheInvalidationRecord(BaseModel):
    cache_family: str
    cache_key: str
    invalidated_at: datetime
    reason: str

class IncrementalPlanRecord(BaseModel):
    plan_id: str
    strategy: str
    affected_entities: List[str]
    estimated_cost: float

class RecomputeDecisionRecord(BaseModel):
    decision: str
    reason: str
    cost_estimate: float

class LazyLoadRecord(BaseModel):
    handle_id: str
    loaded_at: datetime
    bytes_loaded: int

class RuntimeEfficiencyRecord(BaseModel):
    run_id: str
    total_duration_ms: float
    cache_hit_rate: float
    incremental_vs_full_ratio: float

class BottleneckRecord(BaseModel):
    component: str
    step: str
    duration_ms: float
    impact_score: float

class PerformanceManifest(BaseModel):
    run_id: str
    timestamp: datetime
    mode: str
    efficiency: RuntimeEfficiencyRecord
    bottlenecks: List[BottleneckRecord]

class CacheHealthRecord(BaseModel):
    family: str
    total_entries: int
    stale_entries: int
    size_mb: float

class MaterializationRecord(BaseModel):
    handle_id: str
    materialized_at: datetime

class IncrementalScopeRecord(BaseModel):
    scope_id: str
    affected_windows: List[str]

class ChangeSetRecord(BaseModel):
    changes: List[str]

class AffectedEntityRecord(BaseModel):
    entity_id: str
    change_type: str

class PartialMaterializationRecord(BaseModel):
    entity_id: str
    materialized_fields: List[str]

class CacheHealthSummary(BaseModel):
    families: List[CacheHealthRecord]

class CacheAnomalyRecord(BaseModel):
    anomaly_type: str
    description: str
