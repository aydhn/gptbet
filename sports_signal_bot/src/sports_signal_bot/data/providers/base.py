from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
from sports_signal_bot.data.contracts.canonical import (
    CanonicalEventRecord,
    CanonicalOddsRecord,
    CanonicalTeamStatsRecord,
    CanonicalAvailabilityRecord
)
from sports_signal_bot.core.constants import SportType

class BaseProvider(ABC):
    @property
    @abstractmethod
    def provider_name(self) -> str:
        pass

    @abstractmethod
    def sport_support(self) -> List[SportType]:
        pass

    @abstractmethod
    def healthcheck(self) -> bool:
        pass

    @abstractmethod
    def supports_incremental_fetch(self) -> bool:
        pass

class BaseFixtureProvider(BaseProvider):
    @abstractmethod
    def fetch_fixtures(self, sport: SportType, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[dict]:
        """Fetches raw fixtures data as a list of dicts"""
        pass

class BaseOddsProvider(BaseProvider):
    @abstractmethod
    def fetch_odds(self, sport: SportType, event_ids: Optional[List[str]] = None) -> List[dict]:
        """Fetches raw odds data as a list of dicts"""
        pass

class BaseStatsProvider(BaseProvider):
    @abstractmethod
    def fetch_team_stats(self, sport: SportType) -> List[dict]:
         """Fetches raw team stats data as a list of dicts"""
         pass

class BaseAvailabilityProvider(BaseProvider):
    @abstractmethod
    def fetch_availability(self, sport: SportType) -> List[dict]:
        pass
