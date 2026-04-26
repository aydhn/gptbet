from datetime import datetime, timedelta

import pytest

from sports_signal_bot.backtest.contracts import BacktestLedgerRecord, SettlementStatus
from sports_signal_bot.backtest.periods import PeriodSummarizer
from sports_signal_bot.policy.contracts import ActionClass, PolicySignalStatus


def _create_ledger(dt: datetime, executed: bool, status: SettlementStatus):
    return BacktestLedgerRecord(
        event_id="1",
        sport="football",
        market_type="1x2",
        event_datetime_utc=dt,
        decision_timestamp_utc=dt,
        selection="home",
        signal_status=PolicySignalStatus.APPROVED,
        action_class=ActionClass.APPROVED_CANDIDATE,
        threshold_policy_name="def",
        policy_name="test",
        executed_flag=executed,
        execution_reason="ok",
        result_status=status,
        run_id="run1",
    )


def test_daily_summaries():
    now = datetime(2024, 1, 1, 12, 0, 0)
    summarizer = PeriodSummarizer()

    records = [
        _create_ledger(now, True, SettlementStatus.SETTLED_WIN),
        _create_ledger(now, True, SettlementStatus.SETTLED_LOSS),
        _create_ledger(now + timedelta(days=1), True, SettlementStatus.SETTLED_WIN),
    ]

    summaries = summarizer.summarize_by_period(records, "daily")
    assert len(summaries) == 2
    assert summaries[0].period_label == "2024-01-01"
    assert summaries[0].executed_count == 2
    assert summaries[0].hit_rate == 0.5

    assert summaries[1].period_label == "2024-01-02"
    assert summaries[1].executed_count == 1
    assert summaries[1].hit_rate == 1.0
