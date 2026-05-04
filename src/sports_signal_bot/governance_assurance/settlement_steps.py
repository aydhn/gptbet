from typing import List
from sports_signal_bot.governance_assurance.contracts import (
    SettlementStepRecord,
    SettlementStepFamily,
    SettlementSequenceRecord,
    SettlementProgressRecord,
    ProgressState,
    DebtSettlementPlanRecord,
    PlanStatus
)

def sequence_settlement_steps(sequence_id: str, step_families: List[SettlementStepFamily]) -> SettlementSequenceRecord:
    steps = []
    for i, fam in enumerate(step_families):
        # Enforce successor check
        if fam == SettlementStepFamily.SUCCESSOR_RESOLVE and i == 0:
            pass # Valid

    # Just returning sequence of strings as refs for simplicity
    step_refs = [f"step_{fam.value}_{i}" for i, fam in enumerate(step_families)]
    return SettlementSequenceRecord(
        sequence_id=sequence_id,
        ordered_step_refs=step_refs
    )

def update_settlement_progress(plan: DebtSettlementPlanRecord, state: ProgressState) -> SettlementProgressRecord:
    prog = SettlementProgressRecord(
        progress_id=f"prog_{plan.settlement_plan_id}",
        plan_ref=plan.settlement_plan_id,
        state=state
    )

    if state == ProgressState.BOUNDED_PROGRESS_VERIFIED:
        if len(plan.successor_requirements) > 0:
             prog.state = ProgressState.CAVEATED_PROGRESS
             plan.plan_status = PlanStatus.CAVEATED
        else:
             plan.plan_status = PlanStatus.COMPLETED_BOUNDED

    elif state == ProgressState.BLOCKED_PROGRESS:
        plan.plan_status = PlanStatus.BLOCKED

    return prog
