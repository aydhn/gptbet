from typing import List
from abc import ABC, abstractmethod
from datetime import datetime
from .contracts import EventRecord, OddsRecord, TeamStatsRecord

class BaseScheduleProvider(ABC):
    @abstractmethod
    def get_events(self, start_date: datetime, end_date: datetime) -> List[EventRecord]:
        pass

class BaseOddsProvider(ABC):
    @abstractmethod
    def get_odds(self, event_ids: List[str]) -> List[OddsRecord]:
        pass

class BaseStatsProvider(ABC):
    @abstractmethod
    def get_team_stats(self, team_id: str) -> List[TeamStatsRecord]:
        pass

class BaseMarketProvider(ABC):
    @abstractmethod
    def get_market_data(self, event_id: str) -> dict:
        pass
