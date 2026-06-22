from typing import Any, Dict, List, Optional

from .contracts import (
    ComplianceGateRecord,
    ConformanceResultRecord,
    DriftAttestationRecord,
    DriftOutcome,
    GateEvaluationInput,
    GateOutcome,
    PolicyLintRecord,
    SeverityLevel,
)


class ComplianceGateEvaluator:
    def __init__(self):
        pass

    def evaluate_gate(self, input_record: GateEvaluationInput) -> ComplianceGateRecord:

        outcome = GateOutcome.PASS
        reasons = []

        # Check conformance
        for res in input_record.conformance_results:
            if not res.passed:
                if res.severity == SeverityLevel.CRITICAL:
                    outcome = GateOutcome.BLOCKED_CRITICAL
                    reasons.append(f"Critical assertion failed: {res.case_id}")
                elif (
                    res.severity == SeverityLevel.ERROR
                    and outcome != GateOutcome.BLOCKED_CRITICAL
                ):
                    outcome = GateOutcome.BLOCKED
                    reasons.append(f"Error assertion failed: {res.case_id}")
                elif outcome not in [GateOutcome.BLOCKED, GateOutcome.BLOCKED_CRITICAL]:
                    outcome = GateOutcome.PASS_WITH_WARNINGS
                    reasons.append(f"Warning assertion failed: {res.case_id}")

        # Check lint
        if input_record.lint_record and not input_record.lint_record.passed:
            if outcome not in [GateOutcome.BLOCKED, GateOutcome.BLOCKED_CRITICAL]:
                outcome = GateOutcome.BLOCKED
            reasons.append("Linting failed.")

        # Check drift
        for drift in input_record.drift_records:
            if drift.outcome == DriftOutcome.CRITICAL_DRIFT:
                outcome = GateOutcome.BLOCKED_CRITICAL
                reasons.append("Critical drift detected.")
            elif (
                drift.outcome == DriftOutcome.BLOCKING_DRIFT
                and outcome != GateOutcome.BLOCKED_CRITICAL
            ):
                outcome = GateOutcome.BLOCKED
                reasons.append("Blocking drift detected.")

        return ComplianceGateRecord(
            gate_id=input_record.gate_id,
            gate_family=input_record.gate_family,
            outcome=outcome,
            reason=" | ".join(reasons) if reasons else "Passed all checks.",
        )


def evaluate_compliance_gate(
    gate_id: str, results: List[ConformanceResultRecord]
) -> ComplianceGateRecord:
    evaluator = ComplianceGateEvaluator()
    input_record = GateEvaluationInput(
        gate_id=gate_id, gate_family="generic_gate", conformance_results=results
    )
    return evaluator.evaluate_gate(input_record)


def apply_gate_precedence(gates: List[ComplianceGateRecord]) -> GateOutcome:
    for outcome in [
        GateOutcome.BLOCKED_CRITICAL,
        GateOutcome.BLOCKED,
        GateOutcome.REVIEW_REQUIRED,
        GateOutcome.PASS_WITH_WARNINGS,
    ]:
        if any(g.outcome == outcome for g in gates):
            return outcome
    return GateOutcome.PASS


def resolve_exemption_if_any(
    gate: ComplianceGateRecord, exceptions: List[Any]
) -> ComplianceGateRecord:
    # Dummy logic to handle exemptions
    if gate.outcome in [GateOutcome.BLOCKED, GateOutcome.BLOCKED_CRITICAL]:
        # Cannot exempt critical usually, but for demo:
        pass
    return gate


def explain_gate_outcome(gate: ComplianceGateRecord) -> str:
    return f"Gate {gate.gate_id} ({gate.gate_family}) resulted in {gate.outcome.value}. Reason: {gate.reason}"
