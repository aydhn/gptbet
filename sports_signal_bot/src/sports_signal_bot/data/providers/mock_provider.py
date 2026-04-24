from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from sports_signal_bot.data.providers.base import BaseFixtureProvider, BaseOddsProvider, BaseStatsProvider
from sports_signal_bot.core.constants import SportType
from sports_signal_bot.core.random import get_global_seed
import random

class MockProviderBase:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self._provider_name = self.config.get("name", "mock_provider")
        self.seed = get_global_seed()
        if self.seed:
            random.seed(self.seed)

    @property
    def provider_name(self) -> str:
        return self._provider_name

    def sport_support(self) -> List[SportType]:
        supported = []
        for sport in [SportType.FOOTBALL, SportType.BASKETBALL]:
            if self.config.get(sport.value, {}).get("enabled", False):
                supported.append(sport)
        return supported

    def healthcheck(self) -> bool:
        return True

    def supports_incremental_fetch(self) -> bool:
        return True

class AdvancedMockFixtureProvider(MockProviderBase, BaseFixtureProvider):
    def fetch_fixtures(self, sport: SportType, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[dict]:
        if sport not in self.sport_support():
            return []

        start = start_date or datetime.now()

        events = []
        for i in range(1, 4):
            events.append({
                "source_event_id": f"mock_{sport.value}_{i}",
                "sport": sport.value,
                "league": "mock_league",
                "season": "2023",
                "event_datetime_utc": (start + timedelta(days=i)).isoformat() + "Z",
                "home_team": f"Home_{i}",
                "away_team": f"Away_{i}",
                "status": "UPCOMING",
                "venue": f"Stadium_{i}"
            })
        return events

class AdvancedMockOddsProvider(MockProviderBase, BaseOddsProvider):
    def fetch_odds(self, sport: SportType, event_ids: Optional[List[str]] = None) -> List[dict]:
        if sport not in self.sport_support():
            return []

        target_ids = event_ids or [f"mock_{sport.value}_1", f"mock_{sport.value}_2"]
        odds = []

        for eid in target_ids:
            odds.extend([
                {
                    "source_event_id": eid,
                    "market_type": "1X2" if sport == SportType.FOOTBALL else "moneyline",
                    "bookmaker": "mock_bookie",
                    "snapshot_ts_utc": datetime.now().isoformat() + "Z",
                    "selection": "1" if sport == SportType.FOOTBALL else "home",
                    "decimal_odds": str(round(random.uniform(1.5, 3.0), 2)),
                    "implied_probability": "",
                    "handicap_line": "",
                    "total_line": ""
                },
                {
                    "source_event_id": eid,
                    "market_type": "1X2" if sport == SportType.FOOTBALL else "moneyline",
                    "bookmaker": "mock_bookie",
                    "snapshot_ts_utc": datetime.now().isoformat() + "Z",
                    "selection": "2" if sport == SportType.FOOTBALL else "away",
                    "decimal_odds": str(round(random.uniform(1.5, 3.0), 2)),
                    "implied_probability": "",
                    "handicap_line": "",
                    "total_line": ""
                }
            ])
            if sport == SportType.FOOTBALL:
                 odds.append({
                    "source_event_id": eid,
                    "market_type": "1X2",
                    "bookmaker": "mock_bookie",
                    "snapshot_ts_utc": datetime.now().isoformat() + "Z",
                    "selection": "X",
                    "decimal_odds": str(round(random.uniform(2.5, 4.0), 2)),
                    "implied_probability": "",
                    "handicap_line": "",
                    "total_line": ""
                })
        return odds

class AdvancedMockStatsProvider(MockProviderBase, BaseStatsProvider):
    def fetch_team_stats(self, sport: SportType) -> List[dict]:
         if sport not in self.sport_support():
             return []
         return [
             {
                 "team_id": "Home_1",
                 "team_name": "Home_1",
                 "sport": sport.value,
                 "league": "mock_league",
                 "season": "2023",
                 "rating": "1500",
                 "recent_form": "0.5",
                 "rest_days": "3",
                 "rolling_metrics": ""
             }
         ]
