import uuid
from .contracts import ExecutionReadinessRecord

def compute_execution_readiness(
    session_ref: str,
    approval_completeness: bool,
    scope_boundedness: bool,
    rehearsal_success: bool,
    guard_pass_status: bool,
    rollback_completeness: bool,
    observability_completeness: bool,
    confidence_sufficiency: bool,
    federated_playbook_adaptation_safety: bool,
    no_unresolved_critical_blockers: bool,
    freshness_of_incident_context: bool
) -> ExecutionReadinessRecord:

    blockers = []
    status = "not_ready"

    if not approval_completeness:
        blockers.append("approval_incomplete")
    if not rehearsal_success:
        blockers.append("rehearsal_failed_or_missing")
    if not guard_pass_status:
        blockers.append("guards_not_passed")

    if not blockers:
        status = "staged_execution_preparation_ready"
    else:
        status = "blocked"

    return ExecutionReadinessRecord(
        readiness_id=f"ready_{uuid.uuid4().hex[:8]}",
        session_ref=session_ref,
        status=status,
        approval_completeness=approval_completeness,
        scope_boundedness=scope_boundedness,
        rehearsal_success=rehearsal_success,
        guard_pass_status=guard_pass_status,
        rollback_completeness=rollback_completeness,
        observability_completeness=observability_completeness,
        confidence_sufficiency=confidence_sufficiency,
        federated_playbook_adaptation_safety=federated_playbook_adaptation_safety,
        no_unresolved_critical_blockers=no_unresolved_critical_blockers,
        freshness_of_incident_context=freshness_of_incident_context,
        blockers=blockers
    )
