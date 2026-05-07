from typing import List, Dict, Any
from .contracts import (
    AuditPulseCouncilRecord,
    AuditPulseCouncilFamily,
    AuditPulseCouncilStatus,
    AuditPulseCouncilCaseRecord,
    AuditPulseCouncilEvidenceRecord
)

def build_audit_pulse_council(council_id: str, family: AuditPulseCouncilFamily) -> AuditPulseCouncilRecord:
    return AuditPulseCouncilRecord(
        audit_pulse_council_id=council_id,
        council_family=family,
        council_status=AuditPulseCouncilStatus.council_gapped
    )

def open_audit_pulse_council_case(council: AuditPulseCouncilRecord, case: AuditPulseCouncilCaseRecord) -> AuditPulseCouncilRecord:
    council.case_refs.append(case.case_id)
    return council

def collect_audit_pulse_council_evidence(council: AuditPulseCouncilRecord, evidence: AuditPulseCouncilEvidenceRecord) -> AuditPulseCouncilRecord:
    council.evidence_refs.append(evidence.evidence_id)
    return council

def resolve_audit_pulse_council_case(council: AuditPulseCouncilRecord, evidence_list: List[AuditPulseCouncilEvidenceRecord]) -> AuditPulseCouncilRecord:
    if not evidence_list:
        council.council_status = AuditPulseCouncilStatus.council_gapped
        return council

    all_sufficient = all(e.is_sufficient for e in evidence_list)
    has_caveats = len(council.warnings) > 0

    if not all_sufficient:
        council.council_status = AuditPulseCouncilStatus.council_review_only
    elif has_caveats:
        council.council_status = AuditPulseCouncilStatus.council_caveated
    else:
        council.council_status = AuditPulseCouncilStatus.council_verified

    return council

def summarize_audit_pulse_council(council: AuditPulseCouncilRecord) -> Dict[str, Any]:
    return {
        "id": council.audit_pulse_council_id,
        "status": council.council_status,
        "cases": len(council.case_refs),
        "evidence": len(council.evidence_refs)
    }
