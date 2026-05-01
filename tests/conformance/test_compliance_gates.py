import pytest
from sports_signal_bot.conformance.gates import evaluate_compliance_gate
from sports_signal_bot.conformance.contracts import ConformanceResultRecord, SeverityLevel, GateOutcome

def test_evaluate_compliance_gate_pass():
    res = [ConformanceResultRecord(case_id="1", passed=True, details="", severity=None)]
    gate = evaluate_compliance_gate("gate_1", res)
    assert gate.outcome == GateOutcome.PASS

def test_evaluate_compliance_gate_block():
    res = [ConformanceResultRecord(case_id="2", passed=False, details="", severity=SeverityLevel.CRITICAL)]
    gate = evaluate_compliance_gate("gate_2", res)
    assert gate.outcome == GateOutcome.BLOCKED_CRITICAL
