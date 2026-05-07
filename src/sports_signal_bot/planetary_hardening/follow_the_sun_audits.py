import uuid
from typing import List
from src.sports_signal_bot.planetary_hardening.contracts import (
    FollowTheSunAuditPackRecord,
    AuditPackHandoffRecord,
    AuditPackEvidenceRecord,
    AuditPackGapRecord,
    FollowTheSunAuditWarningRecord
)

def build_follow_the_sun_audit_pack(family: str, evidence: List[AuditPackEvidenceRecord]) -> FollowTheSunAuditPackRecord:
    return FollowTheSunAuditPackRecord(
        follow_the_sun_audit_pack_id=f"fts_{uuid.uuid4().hex[:8]}",
        audit_family=family,
        evidence_refs=evidence,
        audit_status="audit_review_only"
    )

def verify_follow_the_sun_handoff(audit: FollowTheSunAuditPackRecord, handoff: AuditPackHandoffRecord) -> FollowTheSunAuditPackRecord:
    audit.handoff_refs.append(handoff)
    if not handoff.is_replayable:
        audit.warnings.append(FollowTheSunAuditWarningRecord(warning_id=f"warn_{uuid.uuid4().hex[:8]}", message="Non-replayable handoff."))
        audit.audit_status = "audit_caveated"
    return audit

def detect_follow_the_sun_gaps(audit: FollowTheSunAuditPackRecord) -> List[AuditPackGapRecord]:
    gaps = []
    if not audit.handoff_refs:
        gaps.append(AuditPackGapRecord(gap_id=f"gap_{uuid.uuid4().hex[:8]}"))
    return gaps

def verify_follow_the_sun_audit_pack(audit: FollowTheSunAuditPackRecord, reject_stale: bool = True) -> FollowTheSunAuditPackRecord:
    warnings = []
    has_stale = any(e.is_stale for e in audit.evidence_refs)

    if has_stale:
        warnings.append(FollowTheSunAuditWarningRecord(warning_id=f"warn_{uuid.uuid4().hex[:8]}", message="Stale evidence in audit pack."))
        if reject_stale:
            audit.audit_status = "audit_caveated"

    if not audit.evidence_refs:
        warnings.append(FollowTheSunAuditWarningRecord(warning_id=f"warn_{uuid.uuid4().hex[:8]}", message="Empty evidence."))
        audit.audit_status = "audit_gapped"

    gaps = detect_follow_the_sun_gaps(audit)
    audit.gap_refs.extend(gaps)
    if gaps:
        audit.audit_status = "audit_gapped"

    if not warnings and not gaps and audit.evidence_refs:
        audit.audit_status = "audit_verified"

    audit.warnings.extend(warnings)
    return audit

def summarize_follow_the_sun_audit_pack(audit: FollowTheSunAuditPackRecord) -> dict:
    return {
        "id": audit.follow_the_sun_audit_pack_id,
        "family": audit.audit_family,
        "status": audit.audit_status,
        "warnings": [w.message for w in audit.warnings],
        "evidence_count": len(audit.evidence_refs),
        "handoffs_count": len(audit.handoff_refs)
    }
