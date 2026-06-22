import uuid
from .contracts import ExecutionReadinessRecord, ExecutionReadinessInputRecord


def compute_execution_readiness(
    params: ExecutionReadinessInputRecord
) -> ExecutionReadinessRecord:

    blockers = []
    status = "not_ready"

    if not params.approval_completeness:
        blockers.append("approval_incomplete")
    if not params.rehearsal_success:
        blockers.append("rehearsal_failed_or_missing")
    if not params.guard_pass_status:
        blockers.append("guards_not_passed")

    if not blockers:
        status = "staged_execution_preparation_ready"
    else:
        status = "blocked"

    return ExecutionReadinessRecord(
        readiness_id=f"ready_{uuid.uuid4().hex[:8]}",
        session_ref=params.session_ref,
        status=status,
        approval_completeness=params.approval_completeness,
        scope_boundedness=params.scope_boundedness,
        rehearsal_success=params.rehearsal_success,
        guard_pass_status=params.guard_pass_status,
        rollback_completeness=params.rollback_completeness,
        observability_completeness=params.observability_completeness,
        confidence_sufficiency=params.confidence_sufficiency,
        federated_playbook_adaptation_safety=(
            params.federated_playbook_adaptation_safety
        ),
        no_unresolved_critical_blockers=params.no_unresolved_critical_blockers,
        freshness_of_incident_context=params.freshness_of_incident_context,
        blockers=blockers
    )
