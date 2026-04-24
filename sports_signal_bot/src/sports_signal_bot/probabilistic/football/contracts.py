from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime
from sports_signal_bot.core.constants import SportType

class GoalEnvironmentConfig(BaseModel):
    default_league_goal_baseline: float = 2.5
    fallback_goal_baseline: float = 2.5
    home_advantage_goal_bonus: float = 0.2
    lambda_min: float = 0.1
    lambda_max: float = 10.0
    max_goals_cutoff: int = 10
    renormalize_truncated_mass: bool = True
    correct_score_top_k: int = 5
    # For smoothing / blending if needed later
    strength_blend_weight: float = 0.5

class LambdaBuildContext(BaseModel):
    event_id: str
    sport: SportType = SportType.FOOTBALL
    model_name: str = "football_poisson_baseline"
    run_id: str
    timestamp_utc: datetime = Field(default_factory=datetime.utcnow)
    config: GoalEnvironmentConfig = Field(default_factory=GoalEnvironmentConfig)

class GoalLambdaEstimate(BaseModel):
    event_id: str
    home_lambda: float
    away_lambda: float
    expected_total_goals: float
    expected_goal_diff: float
    model_name: str
    feature_sources: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)

class CorrectScoreProbability(BaseModel):
    home_goals: int
    away_goals: int
    probability: float

class ScoreMatrixRecord(BaseModel):
    event_id: str
    model_name: str
    max_goals: int
    matrix_sum: float
    truncated_mass: float
    renormalized: bool
    # We won't store the full matrix here, it's a domain object property
    # But we could store a serialized form if needed.
    warnings: List[str] = Field(default_factory=list)

class FootballProbabilityRecord(BaseModel):
    event_id: str
    market_type: str
    model_name: str
    prediction_timestamp_utc: datetime = Field(default_factory=datetime.utcnow)
    predicted_probabilities: Dict[str, float]
    supporting_metrics: Dict[str, float] = Field(default_factory=dict)
    status: str = "success"
    warnings: List[str] = Field(default_factory=list)
