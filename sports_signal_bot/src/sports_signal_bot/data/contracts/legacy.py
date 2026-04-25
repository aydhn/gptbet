from datetime import datetime
from typing import Dict, Optional

from pydantic import BaseModel


class EventRecord(BaseModel):
    event_id: str
    sport: str
    league: str
    home_team: str
    away_team: str
    kickoff: datetime
    status: str
    home_score: Optional[int] = None
    away_score: Optional[int] = None


class OddsRecord(BaseModel):
    event_id: str
    provider: str
    timestamp: datetime
    market: str
    selections: Dict[str, float]


class TeamStatsRecord(BaseModel):
    team_id: str
    date: datetime
    stats: Dict[str, float]


class PredictionRecord(BaseModel):
    event_id: str
    model_id: str
    predicted_probabilities: Dict[str, float]
    timestamp: datetime


class SignalRecord(BaseModel):
    event_id: str
    signal_type: str
    confidence: float
    recommended_action: str
    timestamp: datetime


class BacktestResultRecord(BaseModel):
    run_id: str
    total_events: int
    accuracy: float
    log_loss: float
    brier_score: float
    roi: Optional[float] = None
