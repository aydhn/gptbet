from typing import List, Dict, Any, Optional
from .contracts import ComplianceGateRecord, GateOutcome, ConformanceResultRecord, PolicyLintRecord, DriftAttestationRecord, DriftOutcome, SeverityLevel

class ComplianceGateEvaluator:
    def __init__(self):
        pass

    def evaluate_gate(self,
                      gate_id: str,
                      gate_family: str,
                      conformance_results: List[ConformanceResultRecord],
                      lint_record: Optional[PolicyLintRecord] = None,
                      drift_records: List[DriftAttestationRecord] = []) -> ComplianceGateRecord:

        outcome = GateOutcome.PASS
        reasons = []

        # Check conformance
        for res in conformance_results:
            if not res.passed:
                if res.severity == SeverityLevel.CRITICAL:
                    outcome = GateOutcome.BLOCKED_CRITICAL
                    reasons.append(f"Critical assertion failed: {res.case_id}")
                elif res.severity == SeverityLevel.ERROR and outcome != GateOutcome.BLOCKED_CRITICAL:
                    outcome = GateOutcome.BLOCKED
                    reasons.append(f"Error assertion failed: {res.case_id}")
                elif outcome not in [GateOutcome.BLOCKED, GateOutcome.BLOCKED_CRITICAL]:
                    outcome = GateOutcome.PASS_WITH_WARNINGS
                    reasons.append(f"Warning assertion failed: {res.case_id}")

        # Check lint
        if lint_record and not lint_record.passed:
            if outcome not in [GateOutcome.BLOCKED, GateOutcome.BLOCKED_CRITICAL]:
                outcome = GateOutcome.BLOCKED
            reasons.append("Linting failed.")

        # Check drift
        for drift in drift_records:
            if drift.outcome == DriftOutcome.CRITICAL_DRIFT:
                outcome = GateOutcome.BLOCKED_CRITICAL
                reasons.append("Critical drift detected.")
            elif drift.outcome == DriftOutcome.BLOCKING_DRIFT and outcome != GateOutcome.BLOCKED_CRITICAL:
                outcome = GateOutcome.BLOCKED
                reasons.append("Blocking drift detected.")

        return ComplianceGateRecord(
            gate_id=gate_id,
            gate_family=gate_family,
            outcome=outcome,
            reason=" | ".join(reasons) if reasons else "Passed all checks."
        )

def evaluate_compliance_gate(gate_id: str, results: List[ConformanceResultRecord]) -> ComplianceGateRecord:
    evaluator = ComplianceGateEvaluator()
    return evaluator.evaluate_gate(gate_id, "generic_gate", results)

def apply_gate_precedence(gates: List[ComplianceGateRecord]) -> GateOutcome:
    for outcome in [GateOutcome.BLOCKED_CRITICAL, GateOutcome.BLOCKED, GateOutcome.REVIEW_REQUIRED, GateOutcome.PASS_WITH_WARNINGS]:
        if any(g.outcome == outcome for g in gates):
            return outcome
    return GateOutcome.PASS

def resolve_exemption_if_any(gate: ComplianceGateRecord, exceptions: List[Any]) -> ComplianceGateRecord:
    # Dummy logic to handle exemptions
    if gate.outcome in [GateOutcome.BLOCKED, GateOutcome.BLOCKED_CRITICAL]:
        # Cannot exempt critical usually, but for demo:
        pass
    return gate

def explain_gate_outcome(gate: ComplianceGateRecord) -> str:
    return f"Gate {gate.gate_id} ({gate.gate_family}) resulted in {gate.outcome.value}. Reason: {gate.reason}"
