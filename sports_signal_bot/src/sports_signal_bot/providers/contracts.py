from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class DataFamily(str, Enum):
    FIXTURES = "fixtures"
    ODDS_SNAPSHOTS = "odds_snapshots"
    RESULTS = "results"
    TEAM_METADATA = "team_metadata"
    STANDINGS_OR_CONTEXT = "standings_or_context"
    HEALTH_METADATA = "health_metadata"


class ProviderKind(str, Enum):
    REMOTE_JSON_API = "remote_json_api"
    LOCAL_FILE_FEED = "local_file_feed"
    NORMALIZED_SNAPSHOT_STORE = "normalized_snapshot_store"
    CACHED_PROXY = "cached_proxy"
    MANUAL_DROPZONE = "manual_dropzone"
    STUB_TEST_PROVIDER = "stub_test_provider"


class ProviderDefinitionRecord(BaseModel):
    provider_name: str
    provider_family: str
    provider_kind: ProviderKind
    supported_sports: List[str]
    supported_markets: List[str]
    supported_data_families: List[DataFamily]
    transport_type: str
    auth_required: bool
    free_source: bool
    default_priority: int
    health_profile: str
    notes: Optional[str] = None


class ProviderCapabilityRecord(BaseModel):
    provider_name: str
    sport: str
    data_family: DataFamily
    supports_history: bool
    supports_live_placeholder: bool = False
    supports_pre_match: bool = True
    supports_incremental_fetch: bool = False
    supports_team_alias_resolution: bool = False
    supports_quality_metadata: bool = False
    warnings: List[str] = Field(default_factory=list)


class UnifiedDataRecord(BaseModel):
    """Base class for unified data records."""

    pass


class UnifiedFixtureRecord(UnifiedDataRecord):
    event_id: str
    sport: str
    league: str
    season: str
    home_team: str
    away_team: str
    kickoff_time: datetime
    event_status: str


class UnifiedOddsRecord(UnifiedDataRecord):
    event_id: str
    sport: str
    market_type: str
    odds_timestamp: datetime
    bookmaker: str
    lines: Dict[str, float]


class UnifiedResultRecord(UnifiedDataRecord):
    event_id: str
    sport: str
    final_outcome: str
    home_score: int
    away_score: int
    status: str
    settlement_fields: Dict[str, Any] = Field(default_factory=dict)


class UnifiedTeamRecord(UnifiedDataRecord):
    team_id: str
    sport: str
    name: str
    aliases: List[str] = Field(default_factory=list)
    league: Optional[str] = None
    country: Optional[str] = None
