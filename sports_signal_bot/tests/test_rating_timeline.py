from datetime import datetime

import pytest

from sports_signal_bot.core.constants import SportType
from sports_signal_bot.data.contracts.canonical import CanonicalEventRecord
from sports_signal_bot.ratings.contracts import RatingConfig
from sports_signal_bot.ratings.elo import EloRatingEngine
from sports_signal_bot.ratings.timeline import RatingTimelineProcessor
from sports_signal_bot.results.contracts import EventResultRecord


def test_timeline_ordering_and_update():
    config = RatingConfig(base_rating=1500.0, k_factor=20.0, scope_mode="global")
    engine = EloRatingEngine(config)
    processor = RatingTimelineProcessor(engine, config)

    # Out of order events
    events = [
        CanonicalEventRecord(
            event_id="e2",
            sport=SportType.FOOTBALL,
            league="L",
            season="S",
            event_datetime_utc=datetime(2023, 1, 2, 12, 0),
            home_team="A",
            away_team="C",
            status="completed",
            source="m",
            source_event_id="m",
        ),
        CanonicalEventRecord(
            event_id="e1",
            sport=SportType.FOOTBALL,
            league="L",
            season="S",
            event_datetime_utc=datetime(2023, 1, 1, 12, 0),
            home_team="A",
            away_team="B",
            status="completed",
            source="m",
            source_event_id="m",
        ),
    ]
    results = [
        EventResultRecord(
            event_id="e2",
            sport=SportType.FOOTBALL,
            status="completed",
            final_home_score=0,
            final_away_score=1,
        ),
        EventResultRecord(
            event_id="e1",
            sport=SportType.FOOTBALL,
            status="completed",
            final_home_score=1,
            final_away_score=0,
        ),
    ]

    snapshots, updates = processor.process_timeline(events, results)

    # e1 should be processed first!
    assert snapshots[0].event_id == "e1"
    assert snapshots[1].event_id == "e2"

    # Before e1, A is 1500
    assert snapshots[0].pre_home_rating == 1500.0

    # A wins e1, gets rating bump (+10). Before e2, A should be 1510
    assert updates[0].event_id == "e1"
    assert updates[0].post_home_rating == 1510.0

    assert snapshots[1].pre_home_rating == 1510.0


def test_cancelled_events_skipped():
    config = RatingConfig()
    processor = RatingTimelineProcessor(EloRatingEngine(config), config)

    events = [
        CanonicalEventRecord(
            event_id="e1",
            sport=SportType.FOOTBALL,
            league="L",
            season="S",
            event_datetime_utc=datetime(2023, 1, 1, 12, 0),
            home_team="A",
            away_team="B",
            status="cancelled",
            source="m",
            source_event_id="m",
        ),
    ]
    results = [
        EventResultRecord(
            event_id="e1",
            sport=SportType.FOOTBALL,
            status="cancelled",
            final_home_score=None,
            final_away_score=None,
        ),
    ]

    snapshots, updates = processor.process_timeline(events, results)

    # Snapshot generated for future feature joining, but no update!
    assert len(snapshots) == 1
    assert len(updates) == 0
