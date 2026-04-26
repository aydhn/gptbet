from datetime import datetime, timedelta
from typing import List, Optional

from sports_signal_bot.core.logger import get_logger
from sports_signal_bot.inference.contracts import EventUniverseRecord

logger = get_logger("EventUniverseBuilder")


class EventUniverseBuilder:
    def __init__(self, schedule_provider=None):
        self.schedule_provider = schedule_provider

    def build_event_universe(
        self,
        target_date: datetime,
        sport: Optional[str] = None,
        lookahead_hours: int = 12,
    ) -> List[EventUniverseRecord]:

        start_time = target_date
        end_time = target_date + timedelta(hours=lookahead_hours)

        # In a real system, this would query the DB. We use a mock or adapter
        if self.schedule_provider:
            raw_events = self.schedule_provider.get_events(start_time, end_time)
        else:
            # Mock behavior for testing/smoke
            raw_events = [
                EventUniverseRecord(
                    event_id="evt_1",
                    sport=sport or "football",
                    event_datetime_utc=start_time + timedelta(hours=1),
                    status="not_started",
                    home_team="Team A",
                    away_team="Team B",
                    supported_markets=["1x2", "ou_2_5"],
                ),
                EventUniverseRecord(
                    event_id="evt_2",
                    sport=sport or "basketball",
                    event_datetime_utc=start_time + timedelta(hours=2),
                    status="not_started",
                    home_team="Team C",
                    away_team="Team D",
                    supported_markets=["moneyline", "spread"],
                ),
            ]

        universe = []
        for evt in raw_events:
            # Handle both MockEvent and EventUniverseRecord
            evt_sport = getattr(evt, "sport", sport or "football")
            if sport and evt_sport != sport:
                continue

            status = getattr(evt, "status", "not_started")
            if status not in ["not_started", "pending"]:
                continue

            if isinstance(evt, EventUniverseRecord):
                universe.append(evt)
            else:
                universe.append(
                    EventUniverseRecord(
                        event_id=evt.event_id,
                        sport=evt_sport,
                        event_datetime_utc=getattr(
                            evt, "event_datetime_utc", start_time + timedelta(hours=1)
                        ),
                        status=status,
                        home_team=evt.home_team,
                        away_team=evt.away_team,
                        supported_markets=[
                            "1x2",
                            "ou_2_5",
                            "moneyline",
                            "spread",
                        ],  # Mock markets
                    )
                )

        logger.info(
            f"Built event universe with {len(universe)} events for target {target_date.isoformat()}"
        )
        return universe

    def filter_pre_match_events(
        self, events: List[EventUniverseRecord], current_time: datetime
    ) -> List[EventUniverseRecord]:
        return [
            e
            for e in events
            if e.event_datetime_utc > current_time
            and e.status in ["not_started", "pending"]
        ]

    def filter_supported_markets(
        self, events: List[EventUniverseRecord], market: str
    ) -> List[EventUniverseRecord]:
        return [e for e in events if market in e.supported_markets]

    def exclude_closed_or_invalid_events(
        self, events: List[EventUniverseRecord]
    ) -> List[EventUniverseRecord]:
        return [
            e for e in events if e.status not in ["finished", "cancelled", "postponed"]
        ]

    def summarize_universe_coverage(self, events: List[EventUniverseRecord]) -> dict:
        return {
            "total_events": len(events),
            "sports": list(set(e.sport for e in events)),
            "earliest_event": min((e.event_datetime_utc for e in events), default=None),
            "latest_event": max((e.event_datetime_utc for e in events), default=None),
        }
