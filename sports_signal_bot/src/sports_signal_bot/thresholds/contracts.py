from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

class ThresholdStrategyType(str, Enum):
    SCORE_ONLY = "score_only"
    SCORE_AND_EDGE = "score_and_edge"
    CONSERVATIVE_QUALITY = "conservative_quality"
    COVERAGE_BALANCED = "coverage_balanced"
    REGIME_AWARE_PLACEHOLDER = "regime_aware_placeholder"

class ThresholdCandidateRecord(BaseModel):
    market_type: str
    sport: str
    score_threshold: float
    edge_threshold: Optional[float] = None

    accepted_count: int
    rejected_count: int
    coverage_rate: float
    acceptance_rate: float

    quality_metrics: Dict[str, float] = Field(default_factory=dict)
    objective_value: float = 0.0

    average_signal_score: float = 0.0
    average_edge: float = 0.0
    average_confidence: float = 0.0
    average_uncertainty_penalty: float = 0.0

    warnings: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class ThresholdOptimizationResult(BaseModel):
    sport: str
    market_type: str
    strategy_used: str

    best_candidate: Optional[ThresholdCandidateRecord] = None
    all_candidates: List[ThresholdCandidateRecord] = Field(default_factory=list)

    objective_name: str
    constraints_applied: Dict[str, Any] = Field(default_factory=dict)

    total_evaluated: int = 0
    warnings: List[str] = Field(default_factory=list)

class ThresholdPolicyRecord(BaseModel):
    policy_name: str
    sport: str
    market_type: str
    signal_strategy: str
    threshold_type: str

    selected_threshold: float
    edge_threshold: Optional[float] = None

    minimum_quality_constraints: Dict[str, float] = Field(default_factory=dict)
    optimization_objective: str
    training_reference_window: str = "all_time"
    fallback_rules: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ThresholdSweepRecord(BaseModel):
    sport: str
    market_type: str
    candidates: List[ThresholdCandidateRecord] = Field(default_factory=list)

class SelectivePredictionRecord(BaseModel):
    event_id: str
    sport: str
    market_type: str
    selection: str

    is_accepted: bool
    rejection_reason: Optional[str] = None

    final_signal_score: float
    edge_estimate: float

    policy_used: str
    threshold_values: Dict[str, float] = Field(default_factory=dict)
    component_snapshots: Dict[str, float] = Field(default_factory=dict)

class ThresholdFrontierRecord(BaseModel):
    sport: str
    market_type: str
    tradeoff_curve: List[Dict[str, float]] = Field(default_factory=list)

class ThresholdManifest(BaseModel):
    run_id: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    sport: str
    market_type: str

    best_policy: Optional[ThresholdPolicyRecord] = None

    total_evaluated_candidates: int = 0

    accepted_count: int = 0
    rejected_count: int = 0

    rejection_reasons_summary: Dict[str, int] = Field(default_factory=dict)
    warnings: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
