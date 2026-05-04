import pytest
from sports_signal_bot.governance_assurance.contracts import (
    SettlementStepFamily, ProgressState, PlanStatus
)
from sports_signal_bot.governance_assurance.settlement_steps import (
    sequence_settlement_steps, update_settlement_progress
)
from sports_signal_bot.governance_assurance.settlement_planners import create_debt_settlement_plan

def test_sequence_settlement_steps():
    seq = sequence_settlement_steps("seq1", [SettlementStepFamily.REPLAY_RECONCILE, SettlementStepFamily.SUCCESSOR_RESOLVE])
    assert len(seq.ordered_step_refs) == 2

def test_update_settlement_progress():
    plan = create_debt_settlement_plan("pl1", ["d1"], False, False)
    prog = update_settlement_progress(plan, ProgressState.BOUNDED_PROGRESS_VERIFIED)
    assert plan.plan_status == PlanStatus.COMPLETED_BOUNDED

    plan_succ = create_debt_settlement_plan("pl2", ["d2"], False, True)
    prog_succ = update_settlement_progress(plan_succ, ProgressState.BOUNDED_PROGRESS_VERIFIED)
    assert plan_succ.plan_status == PlanStatus.CAVEATED # Successor requirement overrides complete to caveated

    prog_blocked = update_settlement_progress(plan_succ, ProgressState.BLOCKED_PROGRESS)
    assert plan_succ.plan_status == PlanStatus.BLOCKED
