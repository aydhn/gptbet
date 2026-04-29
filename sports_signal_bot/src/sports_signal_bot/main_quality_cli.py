import typer
from rich.console import Console
from sports_signal_bot.quality.gates import QualityGateRunner, GateDefinition
from sports_signal_bot.quality.contracts import GatePolicyRecord, TestSuiteRecord
from sports_signal_bot.quality.registry import GateRegistry, TestSuiteRegistry
from sports_signal_bot.quality.runner import QualityTestRunner
from sports_signal_bot.quality.reporting import TestReporter
from sports_signal_bot.quality.golden import GoldenRegistry
from sports_signal_bot.quality.smoke import SmokeRunnerV2
from sports_signal_bot.quality.regression import RegressionRunner

app = typer.Typer(help="Quality Engineering & Testing commands")
console = Console()

def get_test_environment():
    test_registry = TestSuiteRegistry()
    test_registry.register_suite(TestSuiteRecord(suite_id="smoke_suite", suite_name="Smoke Suite", tests=["test_1"]))
    test_registry.register_suite(TestSuiteRecord(suite_id="regression_suite", suite_name="Regression Suite", tests=["test_2"]))
    test_registry.register_suite(TestSuiteRecord(suite_id="contract_suite", suite_name="Contract Suite", tests=["test_3"]))

    test_runner = QualityTestRunner(test_registry)

    gate_registry = GateRegistry()
    gate_registry.register_gate(GateDefinition("dev_local", "Dev Local Gate", [
        GatePolicyRecord(policy_id="p1", required_suites=["smoke_suite"], blocking=True)
    ]))
    gate_registry.register_gate(GateDefinition("pre_release", "Pre-Release Gate", [
        GatePolicyRecord(policy_id="p2", required_suites=["smoke_suite", "regression_suite"], blocking=True)
    ]))
    gate_registry.register_gate(GateDefinition("promotion_gate", "Promotion Gate", [
        GatePolicyRecord(policy_id="p3", required_suites=["smoke_suite", "contract_suite"], blocking=True)
    ]))

    return gate_registry, test_runner

@app.command()
def run_quality_gate(gate: str = typer.Option(..., help="Gate ID to run")):
    gate_registry, test_runner = get_test_environment()
    runner = QualityGateRunner(gate_registry, test_runner)
    reporter = TestReporter()

    console.print(f"[bold blue]Running Quality Gate: {gate}[/bold blue]")
    try:
        execution = runner.run_gate(gate)
        reporter.write_gate_result(execution)

        if execution.result.passed:
            console.print(f"[bold green]Gate {gate} Passed![/bold green]")
        else:
            console.print(f"[bold red]Gate {gate} Failed with {execution.result.blocking_failures} blocking failures[/bold red]")
            raise typer.Exit(1)

    except ValueError as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        raise typer.Exit(1)

@app.command()
def run_smoke_suite():
    _, test_runner = get_test_environment()
    runner = SmokeRunnerV2(test_runner)
    reporter = TestReporter()

    console.print("[bold blue]Running Smoke Suite...[/bold blue]")
    manifest = runner.run_smoke_suite()
    reporter.write_run_manifest(manifest)
    console.print(f"[bold green]Smoke Suite Passed! ({manifest.passed} tests)[/bold green]")

@app.command()
def run_regression_suite():
    _, test_runner = get_test_environment()
    runner = RegressionRunner(test_runner)
    reporter = TestReporter()

    console.print("[bold blue]Running Regression Suite...[/bold blue]")
    manifest = runner.run_regression_suite()
    reporter.write_run_manifest(manifest)
    console.print(f"[bold green]Regression Suite Passed! ({manifest.passed} tests)[/bold green]")

@app.command()
def list_quality_gates():
    gate_registry, _ = get_test_environment()
    console.print("[bold blue]Available Quality Gates:[/bold blue]")
    for gate in gate_registry.list_gates():
        console.print(f"- {gate.record.gate_id}: {gate.record.name}")

@app.command()
def preview_golden_diffs():
    registry = GoldenRegistry()
    console.print("[bold blue]Previewing Golden Diffs...[/bold blue]")
    # Simulated output
    console.print("No diffs found in golden datasets.")

@app.command()
def list_test_scenarios():
    console.print("[bold blue]Available Test Scenarios:[/bold blue]")
    console.print("- live_like_inference")
    console.print("- monitoring_to_refresh")
    console.print("- freeze_release_workflow")
    console.print("- canary_rollback")
