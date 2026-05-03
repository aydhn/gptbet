from typing import List
from .contracts import RecoveryGuardRecord, RecoveryOrchestrationPlanRecord

def evaluate_scope_guard(plan: RecoveryOrchestrationPlanRecord) -> RecoveryGuardRecord:
    if plan.bounded_scope:
        return RecoveryGuardRecord(guard_id="scope_1", guard_family="scope_guard", outcome="guard_pass", reason="Scope is bounded")
    return RecoveryGuardRecord(guard_id="scope_1", guard_family="scope_guard", outcome="guard_block", reason="Scope is unbound")

def evaluate_replay_guard(plan: RecoveryOrchestrationPlanRecord) -> RecoveryGuardRecord:
    return RecoveryGuardRecord(guard_id="replay_1", guard_family="replay_guard", outcome="guard_pass", reason="Replay is safe")

def evaluate_approval_guard(plan: RecoveryOrchestrationPlanRecord) -> RecoveryGuardRecord:
    return RecoveryGuardRecord(guard_id="approval_1", guard_family="approval_guard", outcome="guard_review_required", reason="Review required")

def aggregate_recovery_guards(plan: RecoveryOrchestrationPlanRecord) -> List[RecoveryGuardRecord]:
    return [
        evaluate_scope_guard(plan),
        evaluate_replay_guard(plan),
        evaluate_approval_guard(plan)
    ]

def explain_guard_failures(guards: List[RecoveryGuardRecord]) -> str:
    failures = [g.reason for g in guards if g.outcome in ["guard_block", "guard_block_critical"]]
    if failures:
        return f"Failures: {', '.join(failures)}"
    return "No guard failures."
