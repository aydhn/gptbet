from typing import Optional
from sports_signal_bot.approvals.contracts import (
    ApprovalRequestRecord, ApprovalDecisionRecord, OperatorIdentityRecord, RequestType
)
from sports_signal_bot.approvals.permissions import assert_permission
from sports_signal_bot.approvals.decisions import ApprovalDecisionApplier
from sports_signal_bot.approvals.registry import ApprovalRegistry

class ApprovalRunner:
    """Orchestrates standard approval workflow transitions."""
    def __init__(self, registry: ApprovalRegistry):
        self.registry = registry

    def process_decision(self, request: ApprovalRequestRecord, operator: OperatorIdentityRecord, action: str, note: str) -> ApprovalDecisionRecord:
        # Check permissions based on the request type
        assert_permission(operator, request.request_type)

        if action == "approve":
            decision = ApprovalDecisionApplier.approve(request, operator.operator_id, note)
        elif action == "reject":
            decision = ApprovalDecisionApplier.reject(request, operator.operator_id, note)
        elif action == "defer":
            decision = ApprovalDecisionApplier.defer(request, operator.operator_id, note)
        else:
            raise ValueError(f"Unknown action {action}")

        self.registry.save_request(request) # updated status
        self.registry.save_decision(decision)
        return decision
