from typing import Any
from typing import List, Dict, Optional
from .contracts import ConformanceSuiteRecord, RunMode, ConformanceResultRecord
from .specs import GovernanceSpecRegistry, AssertionRegistry
from .assertions import evaluate_spec_assertion, build_assertion_context, generate_assertion_evidence

class ConformanceSuiteRegistry:
    def __init__(self):
        self.suites: Dict[str, ConformanceSuiteRecord] = {}
        self._initialize_defaults()

    def _initialize_defaults(self):
        s1 = ConformanceSuiteRecord(
            suite_id="suite_policy_01",
            suite_family="policy_conformance_suite",
            suite_name="Core Policy Suite",
            included_specs=["spec_policy_01"],
            target_components=["policy_engine"],
            run_mode=RunMode.PRE_MERGE,
            gate_binding="policy_gate",
            created_at="2023-10-27T00:00:00Z"
        )
        self.register_suite(s1)

    def register_suite(self, suite: ConformanceSuiteRecord):
        self.suites[suite.suite_id] = suite

    def get_suite(self, suite_id: str) -> Optional[ConformanceSuiteRecord]:
        return self.suites.get(suite_id)

    def list_suites(self) -> List[ConformanceSuiteRecord]:
        return list(self.suites.values())

def resolve_suite_run_mode(suite_id: str, registry: ConformanceSuiteRegistry) -> Optional[RunMode]:
    suite = registry.get_suite(suite_id)
    return suite.run_mode if suite else None

def attach_stage_specific_assertions(suite: ConformanceSuiteRecord) -> List[str]:
    # Logic to add assertions based on run mode
    return suite.included_specs

def run_suite(suite_id: str,
              suite_registry: ConformanceSuiteRegistry,
              spec_registry: GovernanceSpecRegistry,
              assertion_registry: AssertionRegistry,
              context: Dict[str, Any]) -> List[ConformanceResultRecord]:
    suite = suite_registry.get_suite(suite_id)
    results = []
    if not suite:
        return results

    for spec_id in suite.included_specs:
        assertions = assertion_registry.resolve_required_assertions(spec_id, spec_registry)
        for assertion in assertions:
            eval_context = build_assertion_context(context)
            passed = evaluate_spec_assertion(assertion, eval_context)
            evidence = generate_assertion_evidence(assertion, passed, eval_context)
            res = ConformanceResultRecord(
                case_id=f"case_{suite_id}_{spec_id}_{assertion.assertion_id}",
                passed=passed,
                details=evidence,
                severity=assertion.failure_severity if not passed else None
            )
            results.append(res)
    return results

def block_invalid_mode_combinations(mode: RunMode, gate: str) -> bool:
    # Dummy logic
    if mode == RunMode.PRE_MERGE and gate == "activation_gate":
        return False
    return True

def summarize_run_mode_requirements(mode: RunMode) -> str:
    return f"Requirements for mode {mode.value}"
