from datetime import datetime

import pytest

from sports_signal_bot.backtest.contracts import BacktestDecisionRecord
from sports_signal_bot.backtest.execution import CandidateAndApprovedExecution
from sports_signal_bot.backtest.runner import BacktestRunner
from sports_signal_bot.labels.contracts import LabelRecord
from sports_signal_bot.markets.enums import LabelValidityStatus, TargetType
from sports_signal_bot.policy.contracts import ActionClass, PolicySignalStatus


def test_full_backtest_runner(tmp_path):
    execution_policy = CandidateAndApprovedExecution()
    runner = BacktestRunner(
        "football", "1x2", execution_policy, output_dir=str(tmp_path)
    )

    now = datetime.utcnow()
    d1 = BacktestDecisionRecord(
        event_id="1",
        sport="football",
        market_type="football_1x2",
        event_datetime_utc=now,
        decision_timestamp_utc=now,
        selection="home",
        signal_status=PolicySignalStatus.APPROVED,
        action_class=ActionClass.APPROVED_CANDIDATE,
        threshold_policy_name="def",
        policy_name="test",
    )
    l1 = LabelRecord(
        event_id="1",
        market_type="football_1x2",
        label_name="1x2",
        target_type=TargetType.MULTICLASS_CLASSIFICATION,
        sport="football",
        validity_status=LabelValidityStatus.VALID,
        target_text="home",
    )

    manifest = runner.run([d1], [l1])

    assert manifest.summary.total_decisions == 1
    assert manifest.summary.executed_decisions == 1
    assert manifest.summary.win_count == 1
    assert manifest.summary.loss_count == 0

    assert len(manifest.action_subsets) > 0
    assert len(manifest.period_summaries) > 0
