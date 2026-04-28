import uuid
from datetime import datetime, timezone
from sports_signal_bot.approvals.contracts import (
    ApprovalDecisionRecord, RequestStatus, ApprovalRequestRecord, ApprovalScope
)

class ApprovalDecisionApplier:
    @staticmethod
    def approve(request: ApprovalRequestRecord, operator_id: str, operator_note: str, rationale_code: str = "ok") -> ApprovalDecisionRecord:
        request.status = RequestStatus.approved
        return ApprovalDecisionRecord(
            decision_id=f"dec_{uuid.uuid4().hex[:8]}",
            request_id=request.request_id,
            operator_id=operator_id,
            decision_type="approve",
            rationale_code=rationale_code,
            operator_note=operator_note,
            effective_scope=request.request_scope,
            execution_authorized=True
        )

    @staticmethod
    def reject(request: ApprovalRequestRecord, operator_id: str, operator_note: str, rationale_code: str = "rejected") -> ApprovalDecisionRecord:
        request.status = RequestStatus.rejected
        return ApprovalDecisionRecord(
            decision_id=f"dec_{uuid.uuid4().hex[:8]}",
            request_id=request.request_id,
            operator_id=operator_id,
            decision_type="reject",
            rationale_code=rationale_code,
            operator_note=operator_note,
            effective_scope=request.request_scope,
            execution_authorized=False
        )

    @staticmethod
    def defer(request: ApprovalRequestRecord, operator_id: str, operator_note: str, rationale_code: str = "deferred") -> ApprovalDecisionRecord:
        request.status = RequestStatus.deferred
        return ApprovalDecisionRecord(
            decision_id=f"dec_{uuid.uuid4().hex[:8]}",
            request_id=request.request_id,
            operator_id=operator_id,
            decision_type="defer",
            rationale_code=rationale_code,
            operator_note=operator_note,
            effective_scope=request.request_scope,
            execution_authorized=False
        )
