from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class InferenceMode(str, Enum):
    PREVIEW = "preview_mode"
    RESEARCH_LIVE_LIKE = "research_live_like_mode"
    CONSERVATIVE_OPS = "conservative_ops_mode"


class SlotDefinitionRecord(BaseModel):
    slot_id: str
    name: str
    lookahead_window_hours: int = 12
    event_inclusion_horizon_hours: int = 2
    freshness_requirement_minutes: int = 60
    allowed_markets: List[str] = Field(default_factory=list)
    artifact_resolution_policy: str = "latest_compatible"
    output_profile: str = "concise_ops"


class InferenceRunContext(BaseModel):
    run_id: str
    run_timestamp_utc: datetime
    slot_id: str
    target_date: str
    inference_mode: InferenceMode
    artifact_snapshot_policy: str
    event_selection_policy: str
    data_freshness_summary: Dict[str, Any] = Field(default_factory=dict)
    warnings: List[str] = Field(default_factory=list)


class EventUniverseRecord(BaseModel):
    event_id: str
    sport: str
    event_datetime_utc: datetime
    status: str
    home_team: str
    away_team: str
    league: Optional[str] = None
    supported_markets: List[str] = Field(default_factory=list)


class ArtifactResolutionRecord(BaseModel):
    artifact_type: str
    resolved_path: Optional[str] = None
    resolved_id: Optional[str] = None
    version: Optional[str] = None
    fallback_used: bool = False
    fallback_reason: Optional[str] = None


class ArtifactChainRecord(BaseModel):
    sport: str
    market_type: str
    feature_config_id: Optional[str] = None
    model_artifact_id: Optional[str] = None
    calibrator_artifact_id: Optional[str] = None
    ensemble_artifact_id: Optional[str] = None
    stacker_artifact_id: Optional[str] = None
    threshold_policy_id: Optional[str] = None
    policy_artifact_id: Optional[str] = None
    sizing_strategy_id: Optional[str] = None
    portfolio_strategy_id: Optional[str] = None
    warnings: List[str] = Field(default_factory=list)
    is_valid: bool = True


class PipelineStepResult(BaseModel):
    step_name: str
    started_at: datetime
    ended_at: datetime
    status: str
    row_counts: Dict[str, int] = Field(default_factory=dict)
    warnings: List[str] = Field(default_factory=list)
    output_paths: Dict[str, str] = Field(default_factory=dict)


class InferenceDecisionPacket(BaseModel):
    event_id: str
    sport: str
    market_type: str
    teams: str
    final_probabilities: Dict[str, float]
    selected_side: Optional[str]
    signal_score: float
    threshold_status: str
    policy_action_class: str
    final_allocated_stake: float
    rationale_summary: str
    key_warnings: List[str] = Field(default_factory=list)
    artifact_chain_summary: Dict[str, str] = Field(default_factory=dict)


class InferenceReviewPacket(BaseModel):
    event_id: str
    sport: str
    market_type: str
    source_selection_diagnostics: Dict[str, Any] = Field(default_factory=dict)
    dynamic_weight_breakdown: Dict[str, float] = Field(default_factory=dict)
    regime_tags: List[str] = Field(default_factory=list)
    data_quality_summary: Dict[str, Any] = Field(default_factory=dict)
    threshold_rationale: str
    policy_rationale_codes: List[str] = Field(default_factory=list)
    sizing_diagnostics: Dict[str, Any] = Field(default_factory=dict)
    portfolio_budget_notes: str


class InferenceDiagnosticsRecord(BaseModel):
    run_id: str
    step_results: List[PipelineStepResult] = Field(default_factory=list)
    system_health_metrics: Dict[str, Any] = Field(default_factory=dict)


class InferenceSnapshotManifest(BaseModel):
    run_context: InferenceRunContext
    universe_size: int
    resolved_artifact_chains: Dict[str, ArtifactChainRecord]
    fallback_counts: Dict[str, int] = Field(default_factory=dict)
    final_action_class_distribution: Dict[str, int] = Field(default_factory=dict)
    warnings: List[str] = Field(default_factory=list)
