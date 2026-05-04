import uuid
from typing import List, Dict
from .contracts import DebtSettlementPlannerRecordV2, SettlementPlanRecordV2, WarningRecord

def build_debt_settlement_planner_v2(planner_family: str) -> DebtSettlementPlannerRecordV2:
    return DebtSettlementPlannerRecordV2(
        settlement_planner_id=f"dsp_{uuid.uuid4()}",
        planner_family=planner_family,
        source_debt_ledger_refs=[],
        source_marketplace_refs=[],
        source_compiler_refs=[],
        active_plan_refs=[],
        sequencing_policy_ref="default_sequencing",
        boundedness_policy_ref="default_boundedness",
        health_status="healthy",
        warnings=[]
    )

def create_settlement_plan_v2(planner: DebtSettlementPlannerRecordV2, settlement_goal: str) -> SettlementPlanRecordV2:
    plan = SettlementPlanRecordV2(
        settlement_plan_id=f"sp_{uuid.uuid4()}",
        source_debt_refs=[],
        source_replay_refs=[],
        source_successor_refs=[],
        settlement_goal=settlement_goal,
        step_refs=[],
        replay_requirements=["req_replay_reconciliation"],
        successor_requirements=["req_successor_resolution"],
        bounded_effect_summary="pending",
        plan_status="plan_built",
        warnings=[]
    )
    planner.active_plan_refs.append(plan.settlement_plan_id)
    return plan

def validate_settlement_plan_v2(plan: SettlementPlanRecordV2) -> bool:
    if not plan.replay_requirements or not plan.successor_requirements:
        plan.plan_status = "plan_blocked"
        return False
    plan.plan_status = "plan_ready_for_bounded_progress"
    return True

def summarize_settlement_planner_v2(planner: DebtSettlementPlannerRecordV2) -> Dict:
    return {
        "id": planner.settlement_planner_id,
        "health": planner.health_status,
        "active_plans": len(planner.active_plan_refs)
    }
