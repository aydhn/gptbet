import uuid
from .contracts import (
    CopilotApprovalRequestRecord,
    CopilotApprovalDecisionRecord,
    CopilotApprovalRequestParams,
)


def build_approval_request(
    params: CopilotApprovalRequestParams,
) -> CopilotApprovalRequestRecord:
    return CopilotApprovalRequestRecord(
        request_id=f"appreq_{uuid.uuid4().hex[:8]}",
        packet_ref=params.packet_ref,
        approval_family=params.approval_family,
        scope=params.scope,
        max_duration_seconds=params.max_duration_seconds,
        allowed_step_families=params.allowed_step_families,
        forbidden_conditions=params.forbidden_conditions,
        rollback_requirement=params.rollback_requirement,
        observability_requirement=params.observability_requirement,
        review_owner=params.review_owner,
    )


def evaluate_approval_scope(
    request: CopilotApprovalRequestRecord, decision_value: str, notes: str
) -> CopilotApprovalDecisionRecord:
    # A simple mock evaluation
    if decision_value == "approved":
        outcome = "approved_for_rehearsal"
    elif decision_value == "denied":
        outcome = "denied"
    else:
        outcome = "review_required"

    return CopilotApprovalDecisionRecord(
        request_ref=request.request_id,
        decision=outcome,
        approved_by="human_approver",
        notes=notes,
        applied_restrictions=[],
    )
