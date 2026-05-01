from typing import List, Dict, Any
from .contracts import ExternalAuditFindingRecord

def derive_local_actions_from_findings(findings: List[ExternalAuditFindingRecord]) -> List[str]:
    actions = []
    for finding in findings:
        if finding.severity == "critical":
            actions.append("open_anomaly_case")
            actions.append("integrity_alert")
        elif finding.severity == "error":
            actions.append("open_review_case")
        elif finding.severity == "warning":
            actions.append("add_supporting_evidence")

    if not actions:
        actions.append("no_change")

    return list(set(actions))

def escalate_external_finding_if_needed(finding: ExternalAuditFindingRecord, context: Dict[str, Any]) -> str:
    if finding.severity == "error" and context.get("is_critical_path"):
        return "critical"
    return finding.severity

def attach_external_finding_to_anomaly_case(finding: ExternalAuditFindingRecord, case_id: str) -> bool:
    # Placeholder for logic to attach a finding to an anomaly case
    return True

def summarize_external_impact(findings: List[ExternalAuditFindingRecord]) -> Dict[str, int]:
    summary = {"critical": 0, "error": 0, "warning": 0, "info": 0}
    for finding in findings:
        if finding.severity in summary:
            summary[finding.severity] += 1
    return summary
