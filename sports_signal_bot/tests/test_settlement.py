import pytest

from sports_signal_bot.core.constants import SportType
from sports_signal_bot.labels.contracts import LabelValidityStatus
from sports_signal_bot.results.contracts import EventResultRecord
from sports_signal_bot.results.resolvers import (resolve_1x2,
                                                 resolve_basketball_moneyline,
                                                 resolve_basketball_totals,
                                                 resolve_btts,
                                                 resolve_over_under)


def test_resolve_1x2():
    rec = EventResultRecord(
        event_id="1",
        sport=SportType.FOOTBALL,
        status="finished",
        final_home_score=2,
        final_away_score=1,
    )
    res, status, _ = resolve_1x2(rec)
    assert res == "home"
    assert status == LabelValidityStatus.VALID

    rec.final_home_score = 1
    res, status, _ = resolve_1x2(rec)
    assert res == "draw"

    rec.final_away_score = 3
    res, status, _ = resolve_1x2(rec)
    assert res == "away"


def test_resolve_over_under():
    rec = EventResultRecord(
        event_id="1",
        sport=SportType.FOOTBALL,
        status="finished",
        final_home_score=2,
        final_away_score=1,
    )
    res, status, _ = resolve_over_under(rec, line=2.5)
    assert res == "over"

    res, status, _ = resolve_over_under(rec, line=3.5)
    assert res == "under"

    res, status, _ = resolve_over_under(rec, line=3.0)
    assert res == "push"
    assert status == LabelValidityStatus.VOID


def test_resolve_btts():
    rec = EventResultRecord(
        event_id="1",
        sport=SportType.FOOTBALL,
        status="finished",
        final_home_score=2,
        final_away_score=1,
    )
    res, status, _ = resolve_btts(rec)
    assert res == "yes"

    rec.final_away_score = 0
    res, status, _ = resolve_btts(rec)
    assert res == "no"


def test_resolve_basketball_moneyline():
    rec = EventResultRecord(
        event_id="1",
        sport=SportType.BASKETBALL,
        status="finished",
        final_home_score=110,
        final_away_score=105,
    )
    res, status, _ = resolve_basketball_moneyline(rec)
    assert res == "home"

    rec.final_away_score = 115
    res, status, _ = resolve_basketball_moneyline(rec)
    assert res == "away"


def test_resolve_missing_scores():
    rec = EventResultRecord(
        event_id="1",
        sport=SportType.FOOTBALL,
        status="finished",
        final_home_score=None,
        final_away_score=None,
    )
    res, status, _ = resolve_1x2(rec)
    assert status == LabelValidityStatus.INVALID

    rec.status = "pending"
    res, status, _ = resolve_1x2(rec)
    assert status == LabelValidityStatus.PENDING

    rec.status = "cancelled"
    res, status, _ = resolve_1x2(rec)
    assert status == LabelValidityStatus.VOID
