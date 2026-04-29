from typing import Any
from typing import Dict, List, Optional
from sports_signal_bot.quality.contracts import TestCaseRecord, TestSuiteRecord
from sports_signal_bot.quality.gates import GateDefinition

class TestSuiteRegistry:
    def __init__(self):
        self.suites: Dict[str, TestSuiteRecord] = {}
        self.tests: Dict[str, TestCaseRecord] = {}

    def register_suite(self, suite: TestSuiteRecord):
        self.suites[suite.suite_id] = suite

    def register_test(self, test: TestCaseRecord):
        self.tests[test.test_id] = test

    def get_suite(self, suite_id: str) -> Optional[TestSuiteRecord]:
        return self.suites.get(suite_id)

class GateRegistry:
    def __init__(self):
        self.gates: Dict[str, GateDefinition] = {}

    def register_gate(self, gate: GateDefinition):
        self.gates[gate.record.gate_id] = gate

    def get_gate(self, gate_id: str) -> Optional[GateDefinition]:
        return self.gates.get(gate_id)

    def list_gates(self) -> List[GateDefinition]:
        return list(self.gates.values())

class ScenarioRegistry:
    def __init__(self):
        self.scenarios = {}

    def register(self, scenario_id: str, data: Any):
        self.scenarios[scenario_id] = data

    def list_scenarios(self):
        return list(self.scenarios.keys())
