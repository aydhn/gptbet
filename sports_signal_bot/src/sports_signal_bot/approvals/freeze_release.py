import uuid
from sports_signal_bot.approvals.contracts import (
    FreezeReleaseRequestRecord, FreezeReleaseDecisionRecord
)

class FreezeReleaseManager:
    @staticmethod
    def create_request(operator_id: str, reason: str, target_component: str = None) -> FreezeReleaseRequestRecord:
        return FreezeReleaseRequestRecord(
            request_id=f"frq_{uuid.uuid4().hex[:8]}",
            operator_id=operator_id,
            reason=reason,
            target_component=target_component
        )

    @staticmethod
    def validate_prerequisites(active_critical_anomalies: int, post_refresh_passed: bool) -> bool:
        """Simple validation for freeze release."""
        if active_critical_anomalies > 0:
            return False
        if not post_refresh_passed:
            return False
        return True

    @staticmethod
    def approve_release(request: FreezeReleaseRequestRecord, operator_id: str, note: str) -> FreezeReleaseDecisionRecord:
        return FreezeReleaseDecisionRecord(
            decision_id=f"fdec_{uuid.uuid4().hex[:8]}",
            request_id=request.request_id,
            operator_id=operator_id,
            approved=True,
            operator_note=note
        )

    @staticmethod
    def deny_release(request: FreezeReleaseRequestRecord, operator_id: str, note: str) -> FreezeReleaseDecisionRecord:
        return FreezeReleaseDecisionRecord(
            decision_id=f"fdec_{uuid.uuid4().hex[:8]}",
            request_id=request.request_id,
            operator_id=operator_id,
            approved=False,
            operator_note=note
        )
