from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum

# --- Overlay Bands ---
class TrustOverlayBand(str, Enum):
    HIGHLY_FRAGILE = "highly_fragile"
    FRAGILE = "fragile"
    CAVEATED = "caveated"
    BOUNDED_RELIABLE = "bounded_reliable"
    RELIABLE_WITH_CAVEATS = "reliable_with_caveats"
    STRONG_BOUNDED_SIGNAL = "strong_bounded_signal"

# --- Mesh Status / Paths / Pressure ---
class MeshEdgeStatus(str, Enum):
    EDGE_ACTIVE = "edge_active"
    EDGE_REVIEW_ONLY = "edge_review_only"
    EDGE_CAVEATED = "edge_caveated"
    EDGE_PRESSURE_HIGH = "edge_pressure_high"
    EDGE_DEGRADED = "edge_degraded"
    EDGE_BLOCKED = "edge_blocked"
    EDGE_SUPERSEDED = "edge_superseded"
    EDGE_EXPIRED = "edge_expired"

class MeshPathOutcome(str, Enum):
    PREFERRED_BOUNDED_PATH = "preferred_bounded_path"
    REVIEW_ONLY_PATH = "review_only_path"
    CAVEATED_PATH = "caveated_path"
    DEGRADED_FALLBACK_PATH = "degraded_fallback_path"
    BLOCKED_PATH = "blocked_path"
    NO_SAFE_MESH_PATH = "no_safe_mesh_path"

class MeshPressureOutcome(str, Enum):
    LOW_PRESSURE = "low_pressure"
    MODERATE_PRESSURE = "moderate_pressure"
    HIGH_PRESSURE = "high_pressure"
    CRITICAL_PRESSURE = "critical_pressure"
    SUPPRESS_NONCRITICAL_PROJECTION = "suppress_noncritical_projection"

# --- Signal Relevance ---
class MarketplaceSignalRelevanceBand(str, Enum):
    IRRELEVANT = "irrelevant"
    WEAK_HINT = "weak_hint"
    BOUNDED_HINT = "bounded_hint"
    USEFUL_SIGNAL = "useful_signal"
    HIGH_RELEVANCE_BUT_CAVEATED = "high_relevance_but_caveated"
    SUPPRESSED_SIGNAL = "suppressed_signal"

# --- Controller States ---
class ResilienceControllerState(str, Enum):
    MONITORING_NORMAL = "monitoring_normal"
    CAUTION_STATE = "caution_state"
    DEGRADED_STATE = "degraded_state"
    SUPPRESSION_STATE = "suppression_state"
    REROUTE_RECOMMENDED = "reroute_recommended"
    HUB_PRESSURE_STATE = "hub_pressure_state"
    ATTESTATION_GAP_STATE = "attestation_gap_state"
    RECOVERY_MONITORING_STATE = "recovery_monitoring_state"
    BLOCKED_STATE = "blocked_state"

# --- Trust Overlay Records ---

class TrustOverlayLayerRecord(BaseModel):
    layer_id: str
    description: str

class TrustOverlayScopeRecord(BaseModel):
    scope_id: str
    description: str

class TrustOverlayDimensionRecord(BaseModel):
    dimension_id: str
    dimension_family: str
    raw_signal_refs: List[str]
    normalized_score: float
    weighting_ref: str
    freshness_state: str
    caveat_state: str
    warnings: List[str] = Field(default_factory=list)

class TrustOverlayWeightRecord(BaseModel):
    weight_id: str
    value: float

class TrustOverlayPenaltyRecord(BaseModel):
    penalty_id: str
    reason: str
    amount: float

class TrustOverlayProjectionRecord(BaseModel):
    projection_id: str
    description: str

class TrustOverlayDecisionRecord(BaseModel):
    decision_id: str
    action: str

class TrustOverlayLineageRecord(BaseModel):
    lineage_id: str
    trace: List[str]

class TrustOverlayWarningRecord(BaseModel):
    warning_id: str
    message: str

class TrustOverlayManifestRecord(BaseModel):
    manifest_id: str
    timestamp: datetime
    overlay_refs: List[str]

class FederationTrustOverlayRecord(BaseModel):
    overlay_id: str
    overlay_family: str
    target_scope_ref: str
    source_registry_refs: List[str]
    source_hub_refs: List[str]
    dimension_scores: Dict[str, float]
    penalties: List[TrustOverlayPenaltyRecord]
    final_overlay_band: TrustOverlayBand
    final_overlay_score: float
    caveat_refs: List[str]
    currentness_refs: List[str]
    warnings: List[str] = Field(default_factory=list)

# --- Hub Routing Mesh Records ---

class MeshNodeRecord(BaseModel):
    node_id: str
    description: str

class MeshEdgeRecord(BaseModel):
    edge_id: str
    source_hub_ref: str
    target_hub_ref: str
    supported_exchange_scopes: List[str]
    supported_attestation_families: List[str]
    sovereignty_constraints: List[str]
    currentness_state: str
    pressure_state: str
    edge_status: MeshEdgeStatus
    warnings: List[str] = Field(default_factory=list)

class MeshPathRecord(BaseModel):
    path_id: str
    edge_refs: List[str]
    path_outcome: MeshPathOutcome
    warnings: List[str] = Field(default_factory=list)

class MeshRouteDecisionRecord(BaseModel):
    decision_id: str
    path_ref: str
    reason: str

class MeshConstraintRecord(BaseModel):
    constraint_id: str
    description: str

class MeshPressureRecord(BaseModel):
    pressure_id: str
    pressure_outcome: MeshPressureOutcome
    dimensions: Dict[str, float]

class MeshDegradationRecord(BaseModel):
    degradation_id: str
    severity: str

class MeshHealthRecord(BaseModel):
    health_id: str
    status: str

class MeshRoutingManifestRecord(BaseModel):
    manifest_id: str
    mesh_refs: List[str]

class MeshWarningRecord(BaseModel):
    warning_id: str
    message: str

class HubRoutingMeshRecord(BaseModel):
    mesh_id: str
    mesh_family: str
    hub_refs: List[str]
    edge_refs: List[str]
    routing_policy_ref: str
    pressure_state: MeshPressureOutcome
    degradation_state: str
    health_status: str
    warnings: List[str] = Field(default_factory=list)

# --- Baseline Marketplace Signal Records ---

class MarketplaceSignalSourceRecord(BaseModel):
    source_id: str
    description: str

class MarketplaceSignalDimensionRecord(BaseModel):
    dimension_id: str
    description: str

class MarketplaceSignalFreshnessRecord(BaseModel):
    freshness_id: str
    state: str

class MarketplaceSignalRelevanceRecord(BaseModel):
    relevance_id: str
    band: MarketplaceSignalRelevanceBand

class MarketplaceSignalProjectionRecord(BaseModel):
    projection_id: str
    target_ref: str

class MarketplaceSignalDecisionRecord(BaseModel):
    decision_id: str
    action: str

class MarketplaceSignalCatalogRecord(BaseModel):
    catalog_id: str
    entries: List[str]

class MarketplaceSignalManifestRecord(BaseModel):
    manifest_id: str
    signal_refs: List[str]

class MarketplaceSignalWarningRecord(BaseModel):
    warning_id: str
    message: str

class BaselineMarketplaceSignalRecord(BaseModel):
    signal_id: str
    signal_family: str
    source_baseline_ref: str
    target_scope_ref: str
    dimension_refs: List[str]
    freshness_state: str
    relevance_band: MarketplaceSignalRelevanceBand
    caveat_refs: List[str]
    projection_status: str
    warnings: List[str] = Field(default_factory=list)

# --- Marketplace Signal Catalog Records ---
class MarketplaceSignalCatalogEntryRecord(BaseModel):
    entry_id: str
    signal_ref: str

class SignalSourceHealthRecord(BaseModel):
    health_id: str
    source_ref: str
    status: str

class SignalApplicabilityRuleRecord(BaseModel):
    rule_id: str
    description: str

class SignalSuppressionRecord(BaseModel):
    suppression_id: str
    reason: str

# --- Ecosystem Resilience Controller Records ---

class ResilienceControllerScopeRecord(BaseModel):
    scope_id: str
    description: str

class ResilienceControllerSignalRecord(BaseModel):
    signal_id: str
    description: str

class ResilienceControllerDecisionRecord(BaseModel):
    decision_id: str
    action: str

class ResilienceControllerActionRecord(BaseModel):
    action_id: str
    description: str

class ResilienceControllerDegradationRecord(BaseModel):
    degradation_id: str
    severity: str

class ResilienceControllerRecoveryRecord(BaseModel):
    recovery_id: str
    description: str

class ResilienceControllerHealthRecord(BaseModel):
    health_id: str
    status: str

class ResilienceControllerManifestRecord(BaseModel):
    manifest_id: str
    controller_refs: List[str]

class ResilienceControllerWarningRecord(BaseModel):
    warning_id: str
    message: str

class EcosystemResilienceControllerRecord(BaseModel):
    controller_id: str
    controller_family: str
    monitored_overlay_refs: List[str]
    monitored_mesh_refs: List[str]
    monitored_signal_catalog_refs: List[str]
    monitored_ecosystem_refs: List[str]
    decision_policy_ref: str
    current_state: ResilienceControllerState
    warnings: List[str] = Field(default_factory=list)

# --- Participant Extensions ---
class ParticipantTrustOverlayRecord(BaseModel):
    participant_id: str
    overlay_ref: str

class ParticipantMeshEligibilityRecord(BaseModel):
    participant_id: str
    mesh_ref: str
    is_eligible: bool

class ParticipantSignalRoleRecord(BaseModel):
    participant_id: str
    role: str

class ParticipantResilienceStateRecord(BaseModel):
    participant_id: str
    state: str

# --- Resilience Summaries ---
class ResilienceDimensionTrendRecord(BaseModel):
    dimension_id: str
    trend: str

class ResilienceSuppressionBurdenRecord(BaseModel):
    burden_id: str
    count: int

class ResilienceRecoveryProjectionRecord(BaseModel):
    projection_id: str
    estimated_time: str

class EcosystemResilienceScoreSummaryRecord(BaseModel):
    summary_id: str
    overlay_stability_score: float
    hub_health_score: float
    signal_freshness_score: float
    participant_stability_score: float
    federation_hygiene_score: float
    scorecard_variance: float
    suppression_burden: float
    degraded_state_duration: float
    timestamp: datetime
