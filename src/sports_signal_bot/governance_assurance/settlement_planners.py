from typing import List, Dict, Any
from sports_signal_bot.governance_assurance.contracts import (
    ConvergenceDebtSettlementPlannerRecord,
    PlannerFamily,
    DebtSettlementPlanRecord,
    PlanStatus,
    DebtSettlementPlannerWarningRecord
)

def build_debt_settlement_planner(
    planner_id: str,
    planner_family: PlannerFamily,
    debt_ledgers: List[str]
) -> ConvergenceDebtSettlementPlannerRecord:
    return ConvergenceDebtSettlementPlannerRecord(
        settlement_planner_id=planner_id,
        planner_family=planner_family,
        input_debt_ledger_refs=debt_ledgers,
        active_plan_refs=[],
        ranking_policy_ref="default_ranking",
        sequencing_policy_ref="strict_sequencing",
        boundedness_policy_ref="fail_closed_bounding",
        health_status="healthy",
        warnings=[]
    )

def create_debt_settlement_plan(
    plan_id: str,
    debt_refs: List[str],
    replay_required: bool,
    successor_required: bool
) -> DebtSettlementPlanRecord:
    status = PlanStatus.BUILT

    if successor_required:
        status = PlanStatus.SUCCESSOR_REQUIRED
    elif replay_required:
        status = PlanStatus.REPLAY_REQUIRED
    else:
        status = PlanStatus.READY_FOR_BOUNDED_PROGRESS

    return DebtSettlementPlanRecord(
        settlement_plan_id=plan_id,
        source_debt_refs=debt_refs,
        settlement_goal="reduce_debt_ceiling",
        step_refs=[],
        bounded_effect_summary="will_reduce_ceiling_if_completed",
        replay_requirements=["req_replay_1"] if replay_required else [],
        successor_requirements=["req_succ_1"] if successor_required else [],
        plan_status=status,
        warnings=[]
    )

def summarize_settlement_planner(planner: ConvergenceDebtSettlementPlannerRecord) -> Dict[str, Any]:
    return {
        "planner_id": planner.settlement_planner_id,
        "family": planner.planner_family.value,
        "active_plans": len(planner.active_plan_refs),
        "health": planner.health_status
    }
