import pytest
from sports_signal_bot.quality.gates import QualityGateRunner, GateDefinition
from sports_signal_bot.quality.contracts import GatePolicyRecord, TestSuiteRecord
from sports_signal_bot.quality.registry import GateRegistry, TestSuiteRegistry
from sports_signal_bot.quality.runner import QualityTestRunner

def test_quality_gate_runner_success():
    # Setup test env
    test_registry = TestSuiteRegistry()
    test_registry.register_suite(TestSuiteRecord(suite_id="smoke_suite", suite_name="Smoke", tests=["test_1"]))
    test_runner = QualityTestRunner(test_registry)

    gate_registry = GateRegistry()
    gate_registry.register_gate(GateDefinition("dev_local", "Dev Local", [
        GatePolicyRecord(policy_id="p1", required_suites=["smoke_suite"], blocking=True)
    ]))

    runner = QualityGateRunner(gate_registry, test_runner)
    execution = runner.run_gate("dev_local")

    assert execution.result.passed is True
    assert execution.result.blocking_failures == 0

def test_quality_gate_not_found():
    test_registry = TestSuiteRegistry()
    test_runner = QualityTestRunner(test_registry)
    gate_registry = GateRegistry()

    runner = QualityGateRunner(gate_registry, test_runner)

    with pytest.raises(ValueError):
        runner.run_gate("unknown_gate")
