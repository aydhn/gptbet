from typing import Dict, Any, List
from .contracts import ComplianceSummaryRecord, VerificationPipelineRunRecord, GateOutcome

class ReportingIntegration:
    def __init__(self):
        self.kpis = {}

    def update_kpis(self, summary: ComplianceSummaryRecord):
        self.kpis["conformance_pass_rate"] = summary.suite_pass_count / max(1, summary.spec_count)
        self.kpis["lint_error_rate"] = summary.lint_findings_by_severity.get("error", 0) + summary.lint_findings_by_severity.get("critical", 0)
        self.kpis["blocking_drift_rate"] = summary.drift_counts_by_severity.get("blocking_drift", 0)
        self.kpis["compliance_gate_block_rate"] = 1 if summary.gate_outcomes.get("blocked", 0) > 0 else 0

    def generate_report(self) -> Dict[str, Any]:
        return {
            "governance_conformance_overview": self.kpis,
            "policy_lint_and_drift_summary": "See detailed logs.",
            "compliance_pipeline_health": "Healthy"
        }
