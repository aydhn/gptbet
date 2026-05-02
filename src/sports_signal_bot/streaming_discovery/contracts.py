from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime, timezone
import uuid

def utcnow():
    return datetime.now(timezone.utc)

class DiscoveryEventRecord(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    event_family: str
    topic_ref: str
    source_ref: str
    target_ref: Optional[str] = None
    event_time: datetime = Field(default_factory=utcnow)
    freshness_state: str = "current"
    trust_context: Dict[str, Any] = Field(default_factory=dict)
    payload_summary: Dict[str, Any] = Field(default_factory=dict)
    lineage_refs: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)

class EventEnvelopeRecord(BaseModel):
    envelope_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    topic: str
    event_family: str
    source: str
    event_hash: str
    sequence_index: int
    lineage_refs: List[str] = Field(default_factory=list)
    trust_snapshot: Dict[str, Any] = Field(default_factory=dict)
    correlation_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    supersession_refs: Optional[List[str]] = None
    replay_required_flag: bool = False
    observability_tags: Dict[str, str] = Field(default_factory=dict)
    event: DiscoveryEventRecord

class EventCursorRecord(BaseModel):
    consumer_id: str
    topic_ref: str
    last_processed_event_id: str
    lag_events_count: int
    last_processed_at: datetime
    is_stalled: bool = False

class AdaptiveRoutingProfileRecord(BaseModel):
    adaptive_profile_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    base_routing_policy_ref: str
    adaptation_bounds: Dict[str, float]
    trust_sensitivity: float
    freshness_sensitivity: float
    lag_penalty_policy: str
    anomaly_penalty_policy: str
    fallback_policy: str
    current_status: str = "active"
    warnings: List[str] = Field(default_factory=list)

class RoutingAdaptationRecord(BaseModel):
    route_ref: str
    source_ref: str
    adaptation_outcome: str
    weight_adjustment: float
    reasoning: str
    applied_at: datetime = Field(default_factory=utcnow)

class SyncAnomalyClusterRecord(BaseModel):
    cluster_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    cluster_family: str
    member_event_ids: List[str]
    suspected_root_causes: List[str]
    affected_sources: List[str]
    affected_routes: List[str]
    severity: str
    first_seen_at: datetime
    current_status: str = "open"
    warnings: List[str] = Field(default_factory=list)

class TelemetrySignalRecord(BaseModel):
    signal_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    signal_family: str
    source_ref: str
    value: float
    recorded_at: datetime = Field(default_factory=utcnow)

class RouteHealthRecord(BaseModel):
    route_ref: str
    health_score: float
    is_safe: bool
    lag_seconds: float
    conflict_count: int

class EcosystemHealthSnapshotRecord(BaseModel):
    snapshot_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=utcnow)
    active_subscriptions: int
    healthy_sources: int
    degraded_sources: int
    stale_source_count: int
    sync_lag_distribution: Dict[str, float]
    overlay_conflict_burden: int
    anomaly_cluster_count_by_severity: Dict[str, int]
    route_flip_rate: float
    no_safe_route_incidents: int
    quarantine_pressure: float
    health_status: str

class DegradationModeRecord(BaseModel):
    mode_family: str
    triggered_at: datetime = Field(default_factory=utcnow)
    triggers: List[str]
    impact_summary: str
    is_active: bool = True

class ResilienceActionRecord(BaseModel):
    action_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    action_family: str
    target_ref: str
    reasoning: str
    executed_at: datetime = Field(default_factory=utcnow)

class StreamingFabricManifest(BaseModel):
    manifest_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=utcnow)
    processed_events_count: int
    active_clusters: int
    adaptations_applied: int
    health_status: str
    active_degradation_modes: List[str]
    resilience_actions_taken: int
