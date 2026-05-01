from typing import Dict, Any, List
from .contracts import DriftAttestationRecord, DriftEvidenceRecord, DriftOutcome, SeverityLevel

class DriftAttestationRunner:
    def __init__(self):
        pass

    def run_drift_attestation(self, current_state: Dict[str, Any], expected_state: Dict[str, Any]) -> DriftAttestationRecord:
        diffs = []
        outcome = DriftOutcome.NO_DRIFT
        severity = SeverityLevel.INFO

        if current_state.get("policy_version") != expected_state.get("policy_version"):
            diffs.append("policy_version mismatch")
            outcome = DriftOutcome.CRITICAL_DRIFT
            severity = SeverityLevel.CRITICAL

        if current_state.get("public_index_stale", False):
            diffs.append("public index is stale")
            if outcome != DriftOutcome.CRITICAL_DRIFT:
                outcome = DriftOutcome.BLOCKING_DRIFT
                severity = SeverityLevel.ERROR

        evidence = DriftEvidenceRecord(
            baseline_ref="expected_baseline",
            current_ref="current_state",
            diff_summary=", ".join(diffs) if diffs else "No differences found",
            scope="global",
            severity=severity,
            affected_gates=["publication_gate"],
            remediation_hint="Update baseline or state",
            proof_refs=[]
        )

        return DriftAttestationRecord(
            attestation_id="drift_01",
            dimension_id="dim_01",
            outcome=outcome,
            evidence=evidence
        )

def compute_policy_drift(current: Dict, expected: Dict) -> DriftAttestationRecord:
    return DriftAttestationRunner().run_drift_attestation(current, expected)

def compute_publication_drift(current: Dict, expected: Dict) -> DriftAttestationRecord:
    return DriftAttestationRunner().run_drift_attestation(current, expected)

def compute_trust_drift(current: Dict, expected: Dict) -> DriftAttestationRecord:
    return DriftAttestationRunner().run_drift_attestation(current, expected)

def compute_portal_profile_drift(current: Dict, expected: Dict) -> DriftAttestationRecord:
    return DriftAttestationRunner().run_drift_attestation(current, expected)

def summarize_drift_findings(records: List[DriftAttestationRecord]) -> Dict[str, int]:
    summary = {o.value: 0 for o in DriftOutcome}
    for r in records:
        summary[r.outcome.value] += 1
    return summary
