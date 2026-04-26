import json
from datetime import datetime
from pathlib import Path

import pytest

from sports_signal_bot.backtest.contracts import (
    BacktestDecisionRecord,
    BacktestReplayRecord,
    ExecutionEligibility,
    ExecutionEligibilityRecord,
    SettlementRecord,
    SettlementStatus,
)
from sports_signal_bot.backtest.ledger import LedgerWriter
from sports_signal_bot.policy.contracts import ActionClass, PolicySignalStatus


def test_ledger_generation(tmp_path):
    writer = LedgerWriter(tmp_path)

    now = datetime.utcnow()
    decision = BacktestDecisionRecord(
        event_id="1",
        sport="football",
        market_type="1x2",
        event_datetime_utc=now,
        decision_timestamp_utc=now,
        selection="home",
        signal_status=PolicySignalStatus.APPROVED,
        action_class=ActionClass.APPROVED_CANDIDATE,
        threshold_policy_name="def",
        policy_name="test",
    )
    eligibility = ExecutionEligibilityRecord(
        eligibility=ExecutionEligibility.EXECUTABLE, reason="ok"
    )
    settlement = SettlementRecord(
        status=SettlementStatus.SETTLED_WIN, realized_outcome="home", hit_flag=True
    )

    replay = BacktestReplayRecord(
        decision=decision, eligibility=eligibility, settlement=settlement
    )

    ledgers = writer.generate_ledger_records("run1", [replay])
    assert len(ledgers) == 1
    assert ledgers[0].executed_flag is True
    assert ledgers[0].hit_flag is True

    json_path = writer.save_to_json(ledgers, "test.json")
    assert json_path.exists()

    with open(json_path, "r") as f:
        data = json.load(f)
        assert len(data) == 1
        assert data[0]["event_id"] == "1"
