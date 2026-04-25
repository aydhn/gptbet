from datetime import datetime, timedelta
from typing import List

from .contracts.legacy import EventRecord, OddsRecord, TeamStatsRecord
from .interfaces import (BaseOddsProvider, BaseScheduleProvider,
                         BaseStatsProvider)


class MockScheduleProvider(BaseScheduleProvider):
    def get_events(self, start_date: datetime, end_date: datetime) -> List[EventRecord]:
        return [
            EventRecord(
                event_id="mock_1",
                sport="football",
                league="EPL",
                home_team="Arsenal",
                away_team="Chelsea",
                kickoff=datetime.now() + timedelta(days=1),
                status="UPCOMING",
            )
        ]


class MockOddsProvider(BaseOddsProvider):
    def get_odds(self, event_ids: List[str]) -> List[OddsRecord]:
        return [
            OddsRecord(
                event_id=eid,
                provider="mock_bookie",
                timestamp=datetime.now(),
                market="1X2",
                selections={"1": 2.1, "X": 3.4, "2": 3.5},
            )
            for eid in event_ids
        ]


class MockStatsProvider(BaseStatsProvider):
    def get_team_stats(self, team_id: str) -> List[TeamStatsRecord]:
        return [
            TeamStatsRecord(
                team_id=team_id,
                date=datetime.now(),
                stats={"form": 0.8, "rating": 1500.0},
            )
        ]
