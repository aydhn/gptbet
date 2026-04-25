from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from sports_signal_bot.core.constants import LeagueType, MarketType, SportType


class CanonicalEventRecord(BaseModel):
    event_id: str
    sport: SportType
    league: str
    season: str
    event_datetime_utc: datetime
    home_team: str
    away_team: str
    status: str
    venue: Optional[str] = None
    source: str
    source_event_id: str


class CanonicalOddsRecord(BaseModel):
    event_id: str
    market_type: MarketType
    bookmaker: str
    snapshot_ts_utc: datetime
    selection: str
    decimal_odds: float
    implied_probability: float
    handicap_line: Optional[float] = None
    total_line: Optional[float] = None
    raw_payload_metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)


class CanonicalTeamStatsRecord(BaseModel):
    team_id: str
    team_name: str
    sport: SportType
    league: str
    season: str
    rating: Optional[float] = None
    recent_form: Optional[float] = None
    rest_days: Optional[int] = None
    rolling_metrics: Optional[Dict[str, float]] = Field(default_factory=dict)


class CanonicalAvailabilityRecord(BaseModel):
    event_id: str
    team_id: str
    player_name: str
    availability_status: str
    reason: Optional[str] = None
    source: str
