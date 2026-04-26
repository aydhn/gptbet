from datetime import datetime, timedelta

import pytest

from sports_signal_bot.backtest.contracts import BacktestDecisionRecord
from sports_signal_bot.backtest.replay import ReplayPlanner
from sports_signal_bot.labels.contracts import LabelRecord
from sports_signal_bot.markets.enums import LabelValidityStatus, TargetType
from sports_signal_bot.policy.contracts import ActionClass, PolicySignalStatus


def _create_mock_decision(evt_id, d_time, e_time):
    return BacktestDecisionRecord(
        event_id=evt_id,
        sport="football",
        market_type="1x2",
        event_datetime_utc=e_time,
        decision_timestamp_utc=d_time,
        selection="home",
        signal_status=PolicySignalStatus.CANDIDATE,
        action_class=ActionClass.CANDIDATE,
        threshold_policy_name="def",
        policy_name="test",
    )


def _create_mock_label(evt_id):
    return LabelRecord(
        event_id=evt_id,
        market_type="1x2",
        label_name="l",
        target_type=TargetType.BINARY_CLASSIFICATION,
        sport="football",
        validity_status=LabelValidityStatus.VALID,
    )


def test_decision_timestamp_ordering():
    now = datetime.utcnow()
    d1 = _create_mock_decision("1", now, now)
    d2 = _create_mock_decision("2", now - timedelta(hours=1), now)

    l1 = _create_mock_label("1")
    l2 = _create_mock_label("2")

    planner = ReplayPlanner()
    dataset = [(d1, l1), (d2, l2)]

    sorted_ds = planner.build_replay_sequence(dataset)
    assert sorted_ds[0][0].event_id == "2"
    assert sorted_ds[1][0].event_id == "1"


def test_event_datetime_ordering():
    now = datetime.utcnow()
    # Same decision time
    d1 = _create_mock_decision("1", now, now)
    d2 = _create_mock_decision("2", now, now - timedelta(hours=1))

    l1 = _create_mock_label("1")
    l2 = _create_mock_label("2")

    planner = ReplayPlanner()
    dataset = [(d1, l1), (d2, l2)]

    sorted_ds = planner.build_replay_sequence(dataset)
    assert sorted_ds[0][0].event_id == "2"
    assert sorted_ds[1][0].event_id == "1"


def test_event_id_fallback_ordering():
    now = datetime.utcnow()
    # Same decision time, same event time
    d1 = _create_mock_decision("B", now, now)
    d2 = _create_mock_decision("A", now, now)

    l1 = _create_mock_label("B")
    l2 = _create_mock_label("A")

    planner = ReplayPlanner()
    dataset = [(d1, l1), (d2, l2)]

    sorted_ds = planner.build_replay_sequence(dataset)
    assert sorted_ds[0][0].event_id == "A"
    assert sorted_ds[1][0].event_id == "B"
