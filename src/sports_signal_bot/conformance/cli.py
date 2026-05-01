import typer
from typing import Optional
import json

from .pipeline import build_verification_pipeline
from .contracts import RunMode

app = typer.Typer(name="conformance", help="Conformance and Compliance commands.")

@app.command("run-conformance-pass")
def run_conformance_pass(mode: str = "pre_merge"):
    typer.echo(f"Running conformance pass in mode: {mode}")
    pipeline = build_verification_pipeline()
    run_mode = RunMode(mode)

    current_state = {"signature_valid": True, "local_override_freeze": False}
    expected_state = {"policy_version": "1.0"}

    result = pipeline.run_pipeline(run_mode, current_state, expected_state)
    typer.echo(f"Run ID: {result.run_id}")
    typer.echo(f"Final Outcome: {result.final_outcome.value}")

    for stage in result.stages:
        typer.echo(f"Stage: {stage.stage_name} - Status: {stage.status} - {stage.details}")

@app.command("preview-governance-specs")
def preview_governance_specs():
    from .specs import GovernanceSpecRegistry
    registry = GovernanceSpecRegistry()
    typer.echo("Governance Specs:")
    for spec in registry.list_specs():
        typer.echo(f"- {spec.spec_id}: {spec.spec_name} ({spec.spec_family.value})")

@app.command("preview-policy-lint")
def preview_policy_lint():
    from .lint import lint_policy_bundle
    policy = {"has_ambiguous_precedence": True}
    res = lint_policy_bundle(policy)
    typer.echo(f"Lint Passed: {res.passed}")
    for f in res.findings:
        typer.echo(f"- [{f.severity.value}] {f.lint_family}: {f.description}")

@app.command("preview-drift-attestations")
def preview_drift_attestations():
    from .drift import DriftAttestationRunner
    runner = DriftAttestationRunner()
    res = runner.run_drift_attestation({"policy_version": "2.0"}, {"policy_version": "1.0"})
    typer.echo(f"Drift Outcome: {res.outcome.value}")
    typer.echo(f"Diff Summary: {res.evidence.diff_summary}")

@app.command("preview-compliance-gates")
def preview_compliance_gates():
    from .gates import ComplianceGateEvaluator
    from .contracts import ConformanceResultRecord, SeverityLevel
    evaluator = ComplianceGateEvaluator()
    res = [ConformanceResultRecord(case_id="1", passed=False, details="Test fail", severity=SeverityLevel.ERROR)]
    gate = evaluator.evaluate_gate("gate_test", "test_family", res)
    typer.echo(f"Gate Outcome: {gate.outcome.value}")
    typer.echo(f"Reason: {gate.reason}")

@app.command("preview-verification-pipeline-runs")
def preview_verification_pipeline_runs():
    run_conformance_pass("nightly_audit")

@app.command("list-conformance-strategies")
def list_conformance_strategies():
    typer.echo("Available Conformance Strategies:")
    typer.echo("- ConservativeConformanceStrategy")
    typer.echo("- BalancedCompliancePipelineStrategy")
    typer.echo("- LintFirstGovernanceStrategy")
    typer.echo("- DriftSensitiveStrategy")
    typer.echo("- E2EAssuranceStrategy")

if __name__ == "__main__":
    app()
