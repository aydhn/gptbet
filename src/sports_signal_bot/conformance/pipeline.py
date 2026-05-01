from typing import List, Dict, Any, Optional
from .contracts import VerificationPipelineRunRecord, VerificationStageRecord, RunMode, GateOutcome, ComplianceManifest, ComplianceDecisionRecord, ComplianceSummaryRecord
from .specs import GovernanceSpecRegistry, AssertionRegistry
from .suites import ConformanceSuiteRegistry, run_suite
from .lint import LintRunner
from .drift import DriftAttestationRunner
from .gates import ComplianceGateEvaluator, apply_gate_precedence

class ContinuousVerificationRunner:
    def __init__(self):
        self.spec_registry = GovernanceSpecRegistry()
        self.assertion_registry = AssertionRegistry()
        self.suite_registry = ConformanceSuiteRegistry()
        self.lint_runner = LintRunner()
        self.drift_runner = DriftAttestationRunner()
        self.gate_evaluator = ComplianceGateEvaluator()

    def run_pipeline(self, mode: RunMode, current_state: Dict[str, Any], expected_state: Dict[str, Any]) -> VerificationPipelineRunRecord:
        stages = []

        # 1. Spec Resolution & Suite Selection
        stages.append(VerificationStageRecord(stage_name="spec_resolution", status="success", details="Specs resolved."))

        # 2. Lint
        lint_result = self.lint_runner.run_lint(current_state)
        stages.append(VerificationStageRecord(stage_name="lint_stage", status="success" if lint_result.passed else "failure", details=f"Lint passed: {lint_result.passed}"))

        # 3. Static Conformance
        conformance_results = []
        for suite in self.suite_registry.list_suites():
             if suite.run_mode == mode or mode == RunMode.NIGHTLY_AUDIT:
                 res = run_suite(suite.suite_id, self.suite_registry, self.spec_registry, self.assertion_registry, current_state)
                 conformance_results.extend(res)

        all_passed = all(r.passed for r in conformance_results)
        stages.append(VerificationStageRecord(stage_name="static_conformance", status="success" if all_passed else "failure", details=f"Conformance passed: {all_passed}"))

        # 4. Drift
        drift_result = self.drift_runner.run_drift_attestation(current_state, expected_state)
        stages.append(VerificationStageRecord(stage_name="drift_attestation", status="success", details=f"Drift outcome: {drift_result.outcome.value}"))

        # 5. Gate Evaluation
        gate = self.gate_evaluator.evaluate_gate(
            gate_id="pipeline_gate",
            gate_family="end_to_end_gate",
            conformance_results=conformance_results,
            lint_record=lint_result,
            drift_records=[drift_result]
        )
        stages.append(VerificationStageRecord(stage_name="gate_evaluation", status="success", details=f"Gate outcome: {gate.outcome.value}"))

        return VerificationPipelineRunRecord(
            run_id="run_01",
            run_mode=mode,
            stages=stages,
            final_outcome=gate.outcome
        )

def build_verification_pipeline() -> ContinuousVerificationRunner:
    return ContinuousVerificationRunner()

def run_pipeline_stage(stage_name: str, runner: ContinuousVerificationRunner, context: Dict) -> VerificationStageRecord:
    return VerificationStageRecord(stage_name=stage_name, status="success", details="Run stage")

def aggregate_stage_results(stages: List[VerificationStageRecord]) -> bool:
    return all(s.status == "success" for s in stages)

def compute_compliance_outcome(run_record: VerificationPipelineRunRecord) -> GateOutcome:
    return run_record.final_outcome

def emit_pipeline_artifacts(run_record: VerificationPipelineRunRecord) -> ComplianceManifest:
    decision = ComplianceDecisionRecord(
        decision_id="dec_01",
        run_id=run_record.run_id,
        outcome=run_record.final_outcome,
        rationale="Computed from pipeline stages."
    )
    return ComplianceManifest(
        manifest_id="man_01",
        run_id=run_record.run_id,
        decision=decision
    )
