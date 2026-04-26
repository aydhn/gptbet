from datetime import datetime

import pytest

from sports_signal_bot.backtest.contracts import (
    BacktestDecisionRecord,
    SettlementStatus,
)
from sports_signal_bot.backtest.settlement import SettlementEngine
from sports_signal_bot.labels.contracts import LabelRecord
from sports_signal_bot.markets.enums import LabelValidityStatus, TargetType
from sports_signal_bot.policy.contracts import ActionClass, PolicySignalStatus


def test_multiclass_hit():
    engine = SettlementEngine()
    decision = BacktestDecisionRecord(
        event_id="1",
        sport="football",
        market_type="football_1x2",
        event_datetime_utc=datetime.utcnow(),
        decision_timestamp_utc=datetime.utcnow(),
        selection="draw",
        signal_status=PolicySignalStatus.APPROVED,
        action_class=ActionClass.APPROVED_CANDIDATE,
        threshold_policy_name="def",
        policy_name="test",
    )
    label = LabelRecord(
        event_id="1",
        market_type="football_1x2",
        label_name="1x2",
        target_type=TargetType.MULTICLASS_CLASSIFICATION,
        sport="football",
        validity_status=LabelValidityStatus.VALID,
        target_text="draw",
    )
    res = engine.compare_decision_vs_result(decision, label)
    assert res.status == SettlementStatus.SETTLED_WIN
    assert res.hit_flag is True


def test_multiclass_miss():
    engine = SettlementEngine()
    decision = BacktestDecisionRecord(
        event_id="1",
        sport="football",
        market_type="football_1x2",
        event_datetime_utc=datetime.utcnow(),
        decision_timestamp_utc=datetime.utcnow(),
        selection="home",
        signal_status=PolicySignalStatus.APPROVED,
        action_class=ActionClass.APPROVED_CANDIDATE,
        threshold_policy_name="def",
        policy_name="test",
    )
    label = LabelRecord(
        event_id="1",
        market_type="football_1x2",
        label_name="1x2",
        target_type=TargetType.MULTICLASS_CLASSIFICATION,
        sport="football",
        validity_status=LabelValidityStatus.VALID,
        target_text="away",
    )
    res = engine.compare_decision_vs_result(decision, label)
    assert res.status == SettlementStatus.SETTLED_LOSS
    assert res.hit_flag is False
