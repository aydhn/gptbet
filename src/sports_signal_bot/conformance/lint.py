from typing import List, Dict, Any
from .contracts import PolicyLintRecord, LintFindingRecord, SeverityLevel

class LintRunner:
    def __init__(self):
        self.rules = [
            self._ambiguous_precedence_lint,
            self._unsafe_overlay_scope_lint
        ]

    def _ambiguous_precedence_lint(self, policy: Dict[str, Any]) -> List[LintFindingRecord]:
        findings = []
        if policy.get("has_ambiguous_precedence", False):
             findings.append(LintFindingRecord(
                 finding_id="lint_ambig_01",
                 lint_family="ambiguous_precedence_lint",
                 severity=SeverityLevel.CRITICAL,
                 description="Ambiguous rule precedence detected.",
                 target="policy_bundle"
             ))
        return findings

    def _unsafe_overlay_scope_lint(self, policy: Dict[str, Any]) -> List[LintFindingRecord]:
        findings = []
        if policy.get("overlay_widens_scope", False):
            findings.append(LintFindingRecord(
                 finding_id="lint_overlay_01",
                 lint_family="unsafe_overlay_scope_lint",
                 severity=SeverityLevel.ERROR,
                 description="Overlay widens scope unsafely.",
                 target="policy_overlay"
             ))
        return findings

    def run_lint(self, target_state: Dict[str, Any]) -> PolicyLintRecord:
        all_findings = []
        for rule in self.rules:
            all_findings.extend(rule(target_state))

        passed = not any(f.severity in [SeverityLevel.ERROR, SeverityLevel.CRITICAL] for f in all_findings)

        return PolicyLintRecord(
            lint_id="lint_run_01",
            findings=all_findings,
            passed=passed
        )

def lint_policy_bundle(bundle: Dict[str, Any]) -> PolicyLintRecord:
    runner = LintRunner()
    return runner.run_lint(bundle)

def lint_overlay_compatibility(overlay: Dict[str, Any]) -> List[LintFindingRecord]:
    runner = LintRunner()
    return runner._unsafe_overlay_scope_lint(overlay)

def detect_shadowed_rules(bundle: Dict[str, Any]) -> List[LintFindingRecord]:
     return []

def detect_unsafe_scope_expansion(bundle: Dict[str, Any]) -> List[LintFindingRecord]:
     return []

def summarize_lint_findings(record: PolicyLintRecord) -> Dict[str, int]:
    summary = {l.value: 0 for l in SeverityLevel}
    for f in record.findings:
        summary[f.severity.value] += 1
    return summary
