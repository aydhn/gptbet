from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from sports_signal_bot.core.constants import SportType


class RatingConfig(BaseModel):
    base_rating: float = 1500.0
    k_factor: float = 20.0
    home_advantage: float = 0.0
    margin_method: str = "no_margin"
    margin_cap: Optional[float] = None
    season_carryover: float = 1.0
    draw_probability_method: str = "heuristic"
    scope_mode: str = "sport_league"  # global, sport_league, sport_league_season
    neutral_venue_policy: str = "ignore_home_advantage"


class TeamRatingState(BaseModel):
    team_id: str
    sport: SportType
    league: Optional[str] = None
    season: Optional[str] = None
    current_rating: float
    matches_played: int = 0
    last_updated_utc: Optional[datetime] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class RatingSnapshotRecord(BaseModel):
    event_id: str
    sport: SportType
    league: str
    season: str
    event_datetime_utc: datetime
    home_team_id: str
    away_team_id: str
    is_neutral: bool = False
    pre_home_rating: float
    pre_away_rating: float
    home_advantage_applied: float = 0.0
    expected_home_score: float
    expected_away_score: float
    snapshot_generated_utc: datetime = Field(default_factory=datetime.utcnow)


class RatingUpdateRecord(BaseModel):
    event_id: str
    sport: SportType
    event_datetime_utc: datetime
    home_team_id: str
    away_team_id: str
    actual_home_score: float
    actual_away_score: float
    pre_home_rating: float
    pre_away_rating: float
    post_home_rating: float
    post_away_rating: float
    home_rating_diff: float
    away_rating_diff: float
    update_timestamp_utc: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class RatingFeatureRecord(BaseModel):
    event_id: str
    sport: SportType
    home_pre_rating: float
    away_pre_rating: float
    rating_diff: float
    abs_rating_diff: float
    expected_home_result_from_rating: float
    implied_strength_bucket: Optional[str] = None
    rating_uncertainty: Optional[float] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class RatingBuildManifest(BaseModel):
    run_id: str
    sport: SportType
    engine_name: str
    start_time_utc: datetime
    end_time_utc: datetime
    events_processed: int
    teams_updated: int
    config_used: RatingConfig
    errors: List[str] = Field(default_factory=list)
