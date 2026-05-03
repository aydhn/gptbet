import uuid
from datetime import datetime, timedelta, timezone
from .contracts import BoundedExecutionTokenRecord, TokenFamily, RemediationLaneRecord, ReviewAwareExecutionRecord

def build_bounded_execution_token(lane: RemediationLaneRecord, review: ReviewAwareExecutionRecord, duration_sec: int) -> BoundedExecutionTokenRecord:
    now = datetime.now(timezone.utc)

    if review.eligibility_downgraded:
        token_family = TokenFamily.review_only_execution_token
    else:
        token_family = TokenFamily.staged_execution_token

    return BoundedExecutionTokenRecord(
        token_id=f"token_{uuid.uuid4().hex[:8]}",
        token_family=token_family,
        bound_lane_ref=lane.lane_id,
        allowed_step_families=lane.allowed_step_families,
        allowed_scope=lane.incident_family,
        issued_from_approval_ref=review.approval_ref,
        valid_from=now,
        valid_until=now + timedelta(seconds=duration_sec),
        max_execution_window_seconds=duration_sec,
        required_guards=["strict_observability", "rollback_verified"],
        status="active"
    )

def validate_execution_token_scope(token: BoundedExecutionTokenRecord, requested_scope: str, requested_step: str) -> bool:
    if token.status != "active":
        return False
    if datetime.now(timezone.utc) > token.valid_until:
        return False
    if requested_scope != token.allowed_scope:
        return False
    if requested_step not in token.allowed_step_families:
        return False
    return True
