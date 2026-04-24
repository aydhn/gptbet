from typing import List, Optional, Dict, Any
from datetime import datetime
import pandas as pd
from pathlib import Path
from sports_signal_bot.core.constants import SportType
from sports_signal_bot.data.providers.base import BaseFixtureProvider, BaseOddsProvider, BaseStatsProvider
from sports_signal_bot.core.paths import get_data_dir

class FileFixtureProvider(BaseFixtureProvider):
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self._provider_name = self.config.get("name", "file_provider")

    @property
    def provider_name(self) -> str:
        return self._provider_name

    def sport_support(self) -> List[SportType]:
        return [SportType(s) for s in [SportType.FOOTBALL, SportType.BASKETBALL] if s.value in self.config]

    def healthcheck(self) -> bool:
        return True

    def supports_incremental_fetch(self) -> bool:
        return False

    def fetch_fixtures(self, sport: SportType, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None) -> List[dict]:
        if sport.value not in self.config:
            return []

        rel_path = self.config[sport.value].get("fixtures_path")
        if not rel_path:
            return []

        full_path = get_data_dir() / rel_path
        if not full_path.exists():
            return []

        df = pd.read_csv(full_path)
        return df.to_dict('records')

class FileOddsProvider(BaseOddsProvider):
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self._provider_name = self.config.get("name", "file_provider")

    @property
    def provider_name(self) -> str:
        return self._provider_name

    def sport_support(self) -> List[SportType]:
        return [SportType(s) for s in [SportType.FOOTBALL, SportType.BASKETBALL] if s.value in self.config]

    def healthcheck(self) -> bool:
        return True

    def supports_incremental_fetch(self) -> bool:
        return False

    def fetch_odds(self, sport: SportType, event_ids: Optional[List[str]] = None) -> List[dict]:
        if sport.value not in self.config:
            return []

        rel_path = self.config[sport.value].get("odds_path")
        if not rel_path:
            return []

        full_path = get_data_dir() / rel_path
        if not full_path.exists():
            return []

        df = pd.read_csv(full_path)
        if event_ids:
            df = df[df['source_event_id'].isin(event_ids)]
        return df.to_dict('records')

class FileStatsProvider(BaseStatsProvider):
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self._provider_name = self.config.get("name", "file_provider")

    @property
    def provider_name(self) -> str:
        return self._provider_name

    def sport_support(self) -> List[SportType]:
        return [SportType(s) for s in [SportType.FOOTBALL, SportType.BASKETBALL] if s.value in self.config]

    def healthcheck(self) -> bool:
        return True

    def supports_incremental_fetch(self) -> bool:
        return False

    def fetch_team_stats(self, sport: SportType) -> List[dict]:
        if sport.value not in self.config:
            return []

        rel_path = self.config[sport.value].get("stats_path")
        if not rel_path:
            return []

        full_path = get_data_dir() / rel_path
        if not full_path.exists():
            return []

        df = pd.read_csv(full_path)
        return df.to_dict('records')
