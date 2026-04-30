from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class SimulationMode(str, Enum):
    DRY_RUN_PATCH_RENDER = "dry_run_patch_render"
    INFERENCE_SANDBOX_REPLAY = "inference_sandbox_replay"
    POLICY_THRESHOLD_REPLAY = "policy_threshold_replay"
    RECONCILIATION_PROVIDER_REPLAY = "reconciliation_provider_replay"
    BACKTEST_SUBSET_REPLAY = "backtest_subset_replay"
    COMPARATIVE_SLOT_REPLAY = "comparative_slot_replay"
    SHADOW_VARIANT_COMPARISON = "shadow_variant_comparison"

class PatchType(str, Enum):
    CONFIG_VALUE_OVERRIDE = "config_value_override"
    SCOPED_RULE_INSERTION = "scoped_rule_insertion"
    PROVIDER_PRIORITY_OVERRIDE = "provider_priority_override"
    TRUST_WEIGHT_OVERRIDE = "trust_weight_override"
    THRESHOLD_BAND_OVERRIDE = "threshold_band_override"
    RATIONALE_PRIORITY_OVERRIDE = "rationale_priority_override"
    WEIGHTING_COMPONENT_OVERRIDE = "weighting_component_override"
    ALIAS_MEMORY_OVERRIDE = "alias_memory_override"
    ARBITRATION_POLICY_OVERRIDE = "arbitration_policy_override"
    MONITORING_THRESHOLD_OVERRIDE = "monitoring_threshold_override"

class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class MaterialityBand(str, Enum):
    TRIVIAL = "trivial"
    SMALL = "small"
    MODERATE = "moderate"
    LARGE = "large"
    CRITICAL = "critical"

class ComparisonStatus(str, Enum):
    IMPROVED = "improved"
    NEUTRAL = "neutral"
    MIXED = "mixed"
    DEGRADED = "degraded"
    INCONCLUSIVE = "inconclusive"
    INVALID_SIMULATION = "invalid_simulation"

class RecommendationType(str, Enum):
    REJECT_PATCH = "reject_patch"
    KEEP_ADVISORY_ONLY = "keep_advisory_only"
    REQUEST_MORE_DATA = "request_more_data"
    SAFE_FOR_REVIEW = "safe_for_review"
    SAFE_FOR_CANDIDATE_RELEASE_PATH = "safe_for_candidate_release_path"
    NARROW_SCOPE_AND_RETRY = "narrow_scope_and_retry"
    CONFLICTING_EVIDENCE = "conflicting_evidence"

class CandidatePatchRecord(BaseModel):
    patch_id: str
    suggestion_id: str
    target_component_family: str
    target_config_family: str
    patch_type: PatchType
    patch_payload: Dict[str, Any]
    scope: Dict[str, Any]
    sandbox_only: bool = True
    expiry_policy: str
    risk_level: RiskLevel
    supporting_evidence_refs: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)

class SimulationRequestRecord(BaseModel):
    request_id: str
    suggestion_ids: List[str]
    simulation_mode: SimulationMode
    audience_profile: str
    target_sport: Optional[str] = None
    target_market: Optional[str] = None
    replay_window: Dict[str, datetime]
    sample_constraints: Dict[str, Any] = Field(default_factory=dict)
    required_quality_gates: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    warnings: List[str] = Field(default_factory=list)

class SandboxOverrideRecord(BaseModel):
    override_id: str
    patch_id: str
    target: str
    override_payload: Dict[str, Any]
    active: bool = True

class SimulationScopeRecord(BaseModel):
    scope_id: str
    request_id: str
    boundaries: Dict[str, Any]

class SimulationPlanRecord(BaseModel):
    plan_id: str
    request_id: str
    steps: List[str]

class BaselineSnapshotRecord(BaseModel):
    snapshot_id: str
    metrics: Dict[str, float]
    decision_counts: Dict[str, int]

class VariantSnapshotRecord(BaseModel):
    snapshot_id: str
    metrics: Dict[str, float]
    decision_counts: Dict[str, int]

class BeforeAfterMetricRecord(BaseModel):
    metric_name: str
    baseline_value: float
    variant_value: float
    delta: float
    delta_percentage: float

class WhatIfReplayRecord(BaseModel):
    replay_id: str
    changed_decisions: int
    impact_summary: str

class ComparisonUniverseRecord(BaseModel):
    universe_id: str
    is_identical: bool
    sample_size: int
    caveats: List[str] = Field(default_factory=list)

class SimulationComparisonRecord(BaseModel):
    comparison_id: str
    baseline_snapshot_id: str
    variant_snapshot_id: str
    universe_record: ComparisonUniverseRecord
    metrics: List[BeforeAfterMetricRecord]
    materiality_band: MaterialityBand
    materiality_score: float
    status: ComparisonStatus

class SimulationWarningRecord(BaseModel):
    warning_id: str
    message: str
    severity: str

class SimulationRecommendationRecord(BaseModel):
    recommendation_id: str
    comparison_id: str
    recommendation: RecommendationType
    required_gates: List[str]
    rationale: str
    warnings: List[SimulationWarningRecord] = Field(default_factory=list)

class SimulationRunRecord(BaseModel):
    run_id: str
    request_id: str
    status: str
    comparison: Optional[SimulationComparisonRecord] = None
    recommendation: Optional[SimulationRecommendationRecord] = None
    started_at: datetime
    completed_at: Optional[datetime] = None

class SandboxManifest(BaseModel):
    manifest_id: str
    run_id: str
    overrides: List[SandboxOverrideRecord]

class PatchApplicationRecord(BaseModel):
    application_id: str
    patch_id: str
    status: str

class SimulationEvidenceRecord(BaseModel):
    evidence_id: str
    run_id: str
    citations: List[str]

class SimulationClaimRecord(BaseModel):
    claim_id: str
    statement: str
    support_refs: List[str]

class SimulationCitationTrail(BaseModel):
    trail_id: str
    claims: List[SimulationClaimRecord]

class SimulationEvidenceBundleRecord(BaseModel):
    bundle_id: str
    run_id: str
    trail: SimulationCitationTrail

class SandboxStateRecord(BaseModel):
    state_id: str
    active_overrides: List[str]

class SandboxIsolationCheckRecord(BaseModel):
    check_id: str
    is_isolated: bool
    leaks_detected: List[str]

class SandboxNamespaceRecord(BaseModel):
    namespace_id: str
    root_path: str
    state: SandboxStateRecord
