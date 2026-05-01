from typing import List
from .contracts import ComplianceExceptionRecord, ExceptionScopeRecord, ExceptionExpiryRecord, ExceptionApprovalRecord

class ExceptionManager:
    def __init__(self):
        self.exceptions: List[ComplianceExceptionRecord] = []

    def request_exception(self, request_ref: str, scope_desc: str, expiry: str, rationale: str, owner: str) -> ComplianceExceptionRecord:
        ex = ComplianceExceptionRecord(
            exception_id=f"exc_{len(self.exceptions) + 1}",
            request_ref=request_ref,
            scope=ExceptionScopeRecord(scope_id=f"scope_{len(self.exceptions) + 1}", description=scope_desc),
            expiry=ExceptionExpiryRecord(expiry_time=expiry),
            rationale=rationale,
            owner=owner,
            approval=ExceptionApprovalRecord(approver_ref="pending", approval_time=""),
            affected_assertions=[]
        )
        self.exceptions.append(ex)
        return ex

    def approve_exception(self, exception_id: str, approver_ref: str, approval_time: str) -> bool:
        for ex in self.exceptions:
            if ex.exception_id == exception_id:
                ex.approval.approver_ref = approver_ref
                ex.approval.approval_time = approval_time
                return True
        return False
