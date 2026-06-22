from typing import Any, Dict, List

from .contracts import OperatorCalendarAuditRecord


def build_operator_calendar_audit(
    audit_id: str, family: str
) -> OperatorCalendarAuditRecord:
    return OperatorCalendarAuditRecord(
        operator_calendar_audit_id=audit_id,
        audit_family=family,
        region_refs=[],
        coverage_window_refs=[],
        owner_refs=[],
        overlap_refs=[],
        gap_refs=[],
        escalation_reachability_refs=[],
        residue_refs=[],
        audit_status="calendar_verified",
        warnings=[],
    )


def verify_calendar_coverage(audit: OperatorCalendarAuditRecord, window_id: str):
    audit.coverage_window_refs.append(window_id)
    return True


def detect_calendar_gaps(audit: OperatorCalendarAuditRecord, gap_id: str):
    audit.gap_refs.append(gap_id)
    audit.audit_status = "calendar_gapped"
    return audit


def summarize_operator_calendar_audit(
    audit: OperatorCalendarAuditRecord,
) -> Dict[str, Any]:
    return {
        "audit_id": audit.operator_calendar_audit_id,
        "status": audit.audit_status,
        "coverage_windows": len(audit.coverage_window_refs),
        "gaps": len(audit.gap_refs),
    }
