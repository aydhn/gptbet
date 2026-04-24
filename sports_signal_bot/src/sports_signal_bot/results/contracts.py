from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from sports_signal_bot.core.constants import SportType

class EventResultRecord(BaseModel):
    event_id: str
    sport: SportType
    status: str
    final_home_score: Optional[float] = None
    final_away_score: Optional[float] = None
    period_scores: Optional[Dict[str, Dict[str, float]]] = Field(default_factory=dict)
    result_timestamp_utc: Optional[datetime] = None
    result_source: str = "unknown"
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)
