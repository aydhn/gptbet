from datetime import datetime, timedelta
from typing import List, Optional
from .contracts import (
    BreakGlassRecord,
    BreakGlassJustificationRecord,
    BreakGlassExpiryRecord,
    BreakGlassReviewRequirementRecord
)

def issue_break_glass_exception(
    target_ref: str,
    reason: str,
    declared_by: str,
    incident_ref: Optional[str] = None,
    expiry_hours: int = 4
) -> BreakGlassRecord:
    justification = BreakGlassJustificationRecord(
        reason=reason,
        incident_ref=incident_ref,
        declared_by=declared_by
    )

    expiry = BreakGlassExpiryRecord(
        expires_at=datetime.utcnow() + timedelta(hours=expiry_hours),
        action_on_expiry="auto_revoke"
    )

    review = BreakGlassReviewRequirementRecord(
        required_reviewer_groups=["governance_core_signers", "security_review_signers"],
        deadline_seconds=86400  # Must review within 24 hours
    )

    return BreakGlassRecord(
        break_glass_id=f"bg_{datetime.utcnow().timestamp()}",
        target_ref=target_ref,
        justification=justification,
        expiry=expiry,
        review_requirement=review,
        is_active=True,
        created_at=datetime.utcnow()
    )

def validate_break_glass_eligibility(
    record: BreakGlassRecord,
    target_family: str
) -> bool:
    if not record.is_active:
        return False

    if datetime.utcnow() > record.expiry.expires_at:
        return False

    # Example logic to limit break-glass usage only to specific target families
    allowed_families = ["emergency_override", "family_freeze"]
    if target_family not in allowed_families:
        return False

    return True

def expire_break_glass(record: BreakGlassRecord) -> BreakGlassRecord:
    if datetime.utcnow() > record.expiry.expires_at and record.is_active:
        record.is_active = False
    return record

def require_post_break_glass_audit(record: BreakGlassRecord) -> bool:
    # Requires an audit if it's expired but not reviewed
    now = datetime.utcnow()
    deadline = record.created_at + timedelta(seconds=record.review_requirement.deadline_seconds)
    return now > deadline # Or track a "reviewed" boolean
