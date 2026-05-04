from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime
import uuid

# --- OVERLAY EXCHANGE ---
class OverlayExchangeScopeRecord(BaseModel):
    scope_id: str
    allowed_dimensions: List[str]
    max_projection_strength: str
    caveat_requirements: List[str]

class OverlayExchangePacketRecord(BaseModel):
    overlay_exchange_packet_id: str
    source_overlay_ref: str
    source_registry_refs: List[str]
    source_hub_refs: List[str]
    exchange_scope: OverlayExchangeScopeRecord
    projected_dimensions: Dict[str, Any]
    preserved_caveat_refs: List[str]
    currentness_refs: List[str]
    validity_window: Dict[str, datetime]
    replay_support_refs: List[str]
    exchange_status: str
    warnings: List[str]

class TrustOverlayExchangeRecord(BaseModel):
    overlay_exchange_id: str
    source_scope_ref: str
    target_scope_ref: str
    packet_refs: List[OverlayExchangePacketRecord]
    exchange_policy_ref: str
    verification_refs: List[str]
    projection_refs: List[str]
    health_state: str
    warnings: List[str]

# --- MESH ROUTING AT SCALE ---
class MeshPressureSegmentRecord(BaseModel):
    segment_id: str
    pressure_level: str
    queue_depth: int
    degradation_active: bool

class MeshPartitionRecord(BaseModel):
    partition_id: str
    scope_class: str
    sovereignty_restriction_class: str
    pressure_class: str
    route_limits: Dict[str, int]
    active_routes: int
    pressure_segments: List[MeshPressureSegmentRecord]

class MeshTierRecord(BaseModel):
    tier_id: str
    tier_family: str
    participating_hub_refs: List[str]
    supported_exchange_scopes: List[str]
    route_capacity_class: str
    health_policy_ref: str
    degradation_policy_ref: str
    warnings: List[str]

class ScaledHubRoutingMeshRecord(BaseModel):
    scaled_mesh_id: str
    mesh_ref: str
    tier_refs: List[MeshTierRecord]
    partition_refs: List[MeshPartitionRecord]
    route_class_refs: List[str]
    capacity_refs: List[str]
    pressure_segments: List[MeshPressureSegmentRecord]
    health_status: str
    warnings: List[str]

# --- BENCHMARK SIGNAL ECOSYSTEM ---
class SignalCorroborationRecord(BaseModel):
    corroboration_id: str
    band: str
    corroborating_source_refs: List[str]
    conflicting_source_refs: List[str]

class SignalProvenanceRecord(BaseModel):
    provenance_id: str
    originating_baseline_ref: str
    contributing_participant_refs: List[str]
    transformation_path: List[str]
    suppression_history: List[str]
    confidence_cap: str

class SignalEcosystemSourceRecord(BaseModel):
    signal_source_id: str
    source_family: str
    source_ref: str
    supported_signal_families: List[str]
    provenance_confidence: str
    freshness_state: str
    caveat_density: float
    health_state: str
    warnings: List[str]

class BenchmarkSignalEcosystemRecord(BaseModel):
    signal_ecosystem_id: str
    source_catalog_refs: List[SignalEcosystemSourceRecord]
    active_signal_refs: List[str]
    corroboration_refs: List[SignalCorroborationRecord]
    provenance_refs: List[SignalProvenanceRecord]
    suppression_refs: List[str]
    health_status: str
    warnings: List[str]

# --- SOVEREIGN RESILIENCE GOVERNANCE BASELINES ---
class GovernanceBaselineVersionRecord(BaseModel):
    version_id: str
    version_tag: str
    published_at: datetime

class GovernanceBaselineDimensionRecord(BaseModel):
    dimension_name: str
    required_alignment: str
    current_drift: float

class SovereignResilienceGovernanceBaselineRecord(BaseModel):
    governance_baseline_id: str
    baseline_family: str
    applicable_scope_refs: List[str]
    dimension_refs: List[GovernanceBaselineDimensionRecord]
    version_ref: GovernanceBaselineVersionRecord
    validity_window: Dict[str, datetime]
    normalization_policy_ref: str
    baseline_status: str
    warnings: List[str]

# --- CONTROLLER EXTENSIONS ---
class ControllerProjectionCapRecord(BaseModel):
    cap_id: str
    target_dimension: str
    max_value: float
    reason: str

class EcosystemResilienceScaleActionRecord(BaseModel):
    action_id: str
    action_type: str
    target_ref: str
    applied_caps: List[ControllerProjectionCapRecord]
    reason: str
    timestamp: datetime
