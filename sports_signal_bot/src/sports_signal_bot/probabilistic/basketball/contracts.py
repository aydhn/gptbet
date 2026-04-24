from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime
from sports_signal_bot.core.constants import SportType

class BasketballDistributionConfig(BaseModel):
    base_total_points: float = 220.0
    home_advantage_points: float = 3.0
    total_std: float = 14.5
    margin_std: float = 12.0
    pace_weight: float = 1.0
    rating_weight: float = 1.0
    offense_weight: float = 1.0
    defense_weight: float = 1.0
    probability_clip_eps: float = 1e-6
    std_floor: float = 2.0
    default_preview_lines: Dict[str, List[float]] = Field(default_factory=lambda: {
        "totals": [200.5, 210.5, 220.5, 230.5],
        "spreads": [-10.5, -7.5, -5.5, -3.5, -1.5, 1.5, 3.5, 5.5, 7.5, 10.5]
    })

class BasketballScoreEstimate(BaseModel):
    event_id: str
    expected_home_points: float
    expected_away_points: float
    expected_total_points: float
    expected_margin_home: float
    model_name: str
    feature_sources: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)

class BasketballProbabilityRecord(BaseModel):
    event_id: str
    market_type: str
    model_name: str
    prediction_timestamp_utc: datetime = Field(default_factory=datetime.utcnow)
    predicted_probabilities: Dict[str, float]
    supporting_metrics: Dict[str, float] = Field(default_factory=dict)
    status: str = "success"
    warnings: List[str] = Field(default_factory=list)

class BasketballModelDiagnostics(BaseModel):
    event_id: str
    implied_total: float
    implied_margin: float
    total_variance: float
    margin_variance: float
    uncertainty_flags: List[str] = Field(default_factory=list)
    clipping_warnings: List[str] = Field(default_factory=list)
