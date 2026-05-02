from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum

class DeliveryMode(str, Enum):
    snapshot_pull_bridge = "snapshot_pull_bridge"
    event_batch_bridge = "event_batch_bridge"
    periodic_delta_bridge = "periodic_delta_bridge"
    metadata_signal_bridge = "metadata_signal_bridge"
    review_quarantine_bridge = "review_quarantine_bridge"
    simulation_relay_bridge = "simulation_relay_bridge"

class ExternalEventRelayRecord(BaseModel):
    relay_id: str
    relay_family: str
    source_ref: str
    supported_event_families: List[str]
    delivery_mode: DeliveryMode
    integrity_mode: str
    freshness_expectation: str
    review_policy: str
    active_status: str
    warnings: List[str] = Field(default_factory=list)

class RelayEnvelopeRecord(BaseModel):
    envelope_id: str
    relay_id: str
    event_family: str
    source_identity: str
    event_hash: str
    sequence_hint: Optional[int] = None
    freshness_hint: Optional[str] = None
    integrity_hint: Optional[str] = None
    correlation_refs: List[str] = Field(default_factory=list)
    expected_verification_requirements: List[str] = Field(default_factory=list)
    quarantine_defaults: Dict[str, Any] = Field(default_factory=dict)
    lineage_refs: List[str] = Field(default_factory=list)
    payload: Dict[str, Any]

class RelayHealthRecord(BaseModel):
    relay_id: str
    status: str
    delivery_continuity_score: float
    freshness_adherence_score: float
    integrity_verification_success_rate: float
    quarantine_ratio: float
    warnings: List[str] = Field(default_factory=list)

class MirrorSwarmRecord(BaseModel):
    swarm_id: str
    swarm_family: str
    member_mirror_refs: List[str]
    coverage_scope: str
    agreement_policy: str
    lag_policy: str
    split_brain_policy: str
    health_status: str
    warnings: List[str] = Field(default_factory=list)

class SwarmAgreementRecord(BaseModel):
    swarm_id: str
    agreement_result: str
    participating_members: List[str]
    stale_members_excluded: List[str]
    timestamp: datetime
    details: Dict[str, Any]

class TrustLoopCalibrationRecord(BaseModel):
    calibration_id: str
    target_routing_profile_ref: str
    calibration_window: str
    baseline_weights: Dict[str, float]
    proposed_adjustments: Dict[str, float]
    bounded_adjustments: Dict[str, float]
    calibration_evidence_refs: List[str]
    validation_status: str
    warnings: List[str] = Field(default_factory=list)

class GameDaySimulationRecord(BaseModel):
    simulation_id: str
    scenario_family: str
    target_scope: str
    injected_failures: List[str]
    expected_behaviors: List[str]
    observed_behaviors: List[str]
    resilience_score: float
    remediation_refs: List[str]
    warnings: List[str] = Field(default_factory=list)

class ResilienceScorecardRecord(BaseModel):
    scorecard_id: str
    timestamp: datetime
    overall_band: str
    dimensions: Dict[str, float]
    gaps: List[str] = Field(default_factory=list)

class EcosystemResilienceManifest(BaseModel):
    manifest_id: str
    timestamp: datetime
    strategy_used: str
    relays: List[ExternalEventRelayRecord]
    swarms: List[MirrorSwarmRecord]
    recent_calibrations: List[TrustLoopCalibrationRecord]
    recent_simulations: List[GameDaySimulationRecord]
    scorecard: ResilienceScorecardRecord
    recovery_mode_active: bool
    summary_stats: Dict[str, Any]
