from typing import List, Dict, Any, Optional
import datetime
from sports_signal_bot.quality.contracts import (
    QualityGateRecord, GatePolicyRecord, GateExecutionRecord, GateResultRecord, TestRunManifest
)

class GateDefinition:
    def __init__(self, gate_id: str, name: str, policies: List[GatePolicyRecord]):
        self.record = QualityGateRecord(gate_id=gate_id, name=name, policies=policies)

class QualityGateRunner:
    def __init__(self, registry: Any, test_runner: Any):
        self.registry = registry
        self.test_runner = test_runner

    def run_gate(self, gate_id: str) -> GateExecutionRecord:
        gate_def = self.registry.get_gate(gate_id)
        if not gate_def:
            raise ValueError(f"Gate {gate_id} not found")

        execution = GateExecutionRecord(
            execution_id=f"exec_{int(datetime.datetime.now().timestamp())}",
            gate_id=gate_id,
            start_time=datetime.datetime.now().isoformat()
        )

        blocking_failures = 0
        non_blocking_warnings = 0

        for policy in gate_def.record.policies:
            # Simplified: run suites defined in policy
            for suite_id in policy.required_suites:
                manifest = self.test_runner.run_suite(suite_id)
                if manifest.failed > 0:
                    if policy.blocking:
                        blocking_failures += manifest.failed
                    else:
                        non_blocking_warnings += manifest.failed

                if policy.blocking and policy.fail_fast and blocking_failures > 0:
                    break

        passed = blocking_failures == 0
        execution.end_time = datetime.datetime.now().isoformat()
        execution.status = "completed"
        execution.result = GateResultRecord(
            gate_id=gate_id,
            run_id=execution.execution_id,
            timestamp=execution.end_time,
            passed=passed,
            blocking_failures=blocking_failures,
            non_blocking_warnings=non_blocking_warnings
        )

        return execution
