import uuid
from typing import List
from .contracts import CopilotApprovalRequestRecord, CopilotApprovalDecisionRecord

def build_approval_request(
    packet_ref: str,
    approval_family: str,
    scope: str,
    max_duration_seconds: int,
    allowed_step_families: List[str],
    forbidden_conditions: List[str],
    rollback_requirement: str,
    observability_requirement: str,
    review_owner: str
) -> CopilotApprovalRequestRecord:
    return CopilotApprovalRequestRecord(
        request_id=f"appreq_{uuid.uuid4().hex[:8]}",
        packet_ref=packet_ref,
        approval_family=approval_family,
        scope=scope,
        max_duration_seconds=max_duration_seconds,
        allowed_step_families=allowed_step_families,
        forbidden_conditions=forbidden_conditions,
        rollback_requirement=rollback_requirement,
        observability_requirement=observability_requirement,
        review_owner=review_owner
    )

def evaluate_approval_scope(request: CopilotApprovalRequestRecord, decision_value: str, notes: str) -> CopilotApprovalDecisionRecord:
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
        applied_restrictions=[]
    )
