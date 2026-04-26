from datetime import datetime

import pytest

from sports_signal_bot.backtest.contracts import (
    BacktestDecisionRecord,
    ExecutionEligibility,
)
from sports_signal_bot.backtest.execution import (
    ApprovedOnlyExecution,
    CandidateAndApprovedExecution,
    WatchlistShadowExecution,
)
from sports_signal_bot.policy.contracts import ActionClass, PolicySignalStatus


def _create_decision(ac: ActionClass):
    return BacktestDecisionRecord(
        event_id="1",
        sport="f",
        market_type="1",
        event_datetime_utc=datetime.utcnow(),
        decision_timestamp_utc=datetime.utcnow(),
        selection="s",
        signal_status=PolicySignalStatus.PENDING,
        action_class=ac,
        threshold_policy_name="def",
        policy_name="test",
    )


def test_approved_only_execution():
    policy = ApprovedOnlyExecution()
    assert policy.is_executable_decision(
        _create_decision(ActionClass.APPROVED_CANDIDATE)
    )
    assert not policy.is_executable_decision(_create_decision(ActionClass.CANDIDATE))
    assert not policy.is_executable_decision(_create_decision(ActionClass.WATCHLIST))


def test_candidate_and_approved_execution():
    policy = CandidateAndApprovedExecution()
    assert policy.is_executable_decision(
        _create_decision(ActionClass.APPROVED_CANDIDATE)
    )
    assert policy.is_executable_decision(_create_decision(ActionClass.CANDIDATE))
    assert not policy.is_executable_decision(_create_decision(ActionClass.WATCHLIST))


def test_watchlist_shadow_execution():
    policy = WatchlistShadowExecution()
    assert policy.is_executable_decision(
        _create_decision(ActionClass.APPROVED_CANDIDATE)
    )
    assert policy.is_executable_decision(_create_decision(ActionClass.CANDIDATE))
    assert policy.is_executable_decision(_create_decision(ActionClass.WATCHLIST))
    assert not policy.is_executable_decision(
        _create_decision(ActionClass.BLOCKED_CANDIDATE)
    )
