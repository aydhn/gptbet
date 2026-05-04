import pytest
from sports_signal_bot.governance_assurance.contracts import PlannerFamily, PlanStatus
from sports_signal_bot.governance_assurance.settlement_planners import (
    build_debt_settlement_planner, create_debt_settlement_plan, summarize_settlement_planner
)

def test_debt_settlement_planner_creation():
    planner = build_debt_settlement_planner("p1", PlannerFamily.REPLAY_RECONCILIATION, ["d1"])
    assert planner.settlement_planner_id == "p1"

def test_debt_settlement_plan_creation():
    plan_ready = create_debt_settlement_plan("pl1", ["d1"], False, False)
    assert plan_ready.plan_status == PlanStatus.READY_FOR_BOUNDED_PROGRESS

    plan_replay = create_debt_settlement_plan("pl2", ["d1"], True, False)
    assert plan_replay.plan_status == PlanStatus.REPLAY_REQUIRED

    plan_succ = create_debt_settlement_plan("pl3", ["d1"], False, True)
    assert plan_succ.plan_status == PlanStatus.SUCCESSOR_REQUIRED
