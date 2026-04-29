from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from sports_signal_bot.providers.contracts import DataFamily


class ProviderRequestRecord(BaseModel):
    sport: str
    data_family: DataFamily
    market_type: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    league_filter: Optional[str] = None
    event_ids: Optional[List[str]] = None
    team_ids: Optional[List[str]] = None
    incremental_cursor: Optional[str] = None
    freshness_requirements: Dict[str, Any] = Field(default_factory=dict)
    fallback_policy: str = "default"
    quality_minimums: Dict[str, float] = Field(default_factory=dict)
    mode: str = "ops"  # preview, ops, research


def build_provider_request(
    sport: str, data_family: DataFamily, **kwargs
) -> ProviderRequestRecord:
    return ProviderRequestRecord(sport=sport, data_family=data_family, **kwargs)


def validate_provider_request(request: ProviderRequestRecord) -> bool:
    if request.start_date and request.end_date:
        if request.start_date > request.end_date:
            return False
    return True
