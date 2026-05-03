from typing import List
import uuid
from .contracts import RecoveryOrchestrationPlanRecord, RemediationPlaybookRecord, PlaybookStepRecord

def build_recovery_orchestration_plan(playbook: RemediationPlaybookRecord, incident_ref: str) -> RecoveryOrchestrationPlanRecord:
    return RecoveryOrchestrationPlanRecord(
        plan_id=f"plan_{uuid.uuid4().hex[:8]}",
        target_incident_ref=incident_ref,
        selected_playbook_ref=playbook.playbook_id,
        recommended_sequence=sequence_recovery_steps(playbook.steps),
        gating_requirements=["approval_guard"],
        review_requirements=["operator_review"],
        bounded_scope=True,
        rollback_strategy="step_by_step_reversal",
        observability_requirements=["metrics_stable"]
    )

def sequence_recovery_steps(steps: List[PlaybookStepRecord]) -> List[PlaybookStepRecord]:
    return sorted(steps, key=lambda s: s.step_order)

def summarize_recovery_plan(plan: RecoveryOrchestrationPlanRecord) -> str:
    return f"Plan {plan.plan_id} with {len(plan.recommended_sequence)} sequenced steps."
