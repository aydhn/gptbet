from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
from enum import Enum

class WeightComponentRecord(BaseModel):
    trust_score: float = Field(default=0.0, ge=0.0, le=1.0)
    regime_fit_score: float = Field(default=0.0)
    disagreement_penalty: float = Field(default=0.0)
    recency_penalty: float = Field(default=0.0)
    health_score: float = Field(default=0.0)
    family_prior: float = Field(default=0.0)
    calibration_bonus: float = Field(default=0.0)
    combined_score: float = Field(default=0.0)
    explanation: str = Field(default="")

class DynamicWeightRecord(BaseModel):
    event_id: str
    sport: str
    market_type: str
    source_name: str
    source_family: str
    base_weight: float = Field(default=1.0)
    component_scores: WeightComponentRecord
    pre_normalized_weight: float = Field(default=0.0)
    final_weight: float = Field(default=0.0)
    weighting_policy_name: str
    warnings: List[str] = Field(default_factory=list)
    explanation_summary: str = Field(default="")

class SourceWeightBreakdown(BaseModel):
    event_id: str
    weights: List[DynamicWeightRecord]

class WeightingPolicyDefinition(BaseModel):
    name: str
    description: str
    min_weight_floor: float = 0.0
    max_weight_cap: float = 1.0
    score_temperature: float = 1.0
    minimum_peer_count_for_disagreement: int = 3
    regime_sample_damping: float = 1.0
    trust_component_weight: float = 1.0
    regime_component_weight: float = 1.0
    disagreement_penalty_weight: float = 1.0
    recency_penalty_weight: float = 1.0
    health_component_weight: float = 1.0
    calibrated_bonus: float = 0.0

class WeightingDecisionRecord(BaseModel):
    event_id: str
    sport: str
    market_type: str
    policy: str
    decisions: List[DynamicWeightRecord]

class WeightingDiagnosticsRecord(BaseModel):
    event_id: str
    source_count: int
    capped_sources: List[str] = Field(default_factory=list)
    floored_sources: List[str] = Field(default_factory=list)
    stale_penalties: List[str] = Field(default_factory=list)
    fallback_used: bool = False
    average_trust: float = 0.0
    top_source: Optional[str] = None

class WeightingManifest(BaseModel):
    run_id: str
    sport: str
    market_type: str
    event_count: int
    decisions: List[WeightingDecisionRecord]
    diagnostics: List[WeightingDiagnosticsRecord]
