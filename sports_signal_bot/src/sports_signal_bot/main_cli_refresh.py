import typer
from rich.console import Console
from .refresh_controller.runner import RefreshControllerRunner
from .refresh_controller.states import RefreshActionFamily
from .refresh_controller.handlers import (
    catalog_refresh_handler,
    artifact_reresolve_handler,
    snapshot_reselection_handler,
    safe_fallback_handler
)
import json

app = typer.Typer(help="Sports Signal Bot CLI - Refresh Controller Operations")
console = Console()

@app.command("run-refresh-controller")
def run_refresh_controller(
    sport: str = typer.Option(..., help="Target sport"),
    market: str = typer.Option(..., help="Target market"),
    mode: str = typer.Option("normal", help="Operational mode"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Simulate refresh actions without executing")
):
    """Run the refresh controller to process monitoring outputs and execute safe actions."""
    console.print(f"[bold blue]Running Refresh Controller[/bold blue] for {sport}/{market} in {mode} mode (Dry Run: {dry_run})")

    runner = RefreshControllerRunner()
    runner.register_handler(RefreshActionFamily.CATALOG_REFRESH, catalog_refresh_handler)
    runner.register_handler(RefreshActionFamily.RERUN_ARTIFACT_RESOLUTION, artifact_reresolve_handler)
    runner.register_handler(RefreshActionFamily.SNAPSHOT_RESELECTION, snapshot_reselection_handler)
    runner.register_handler(RefreshActionFamily.ENABLE_SAFE_FALLBACK_MODE, safe_fallback_handler)

    # Mock monitor output (in reality this would be loaded from a file or monitoring service)
    monitor_output = {
        "stale_artifact_count": 1 if sport == "football" else 0,
        "data_delay_seconds": 4000 if market == "ou_2_5" else 0,
        "global_health_score": 0.5 if mode == "conservative_ops" else 1.0
    }

    console.print(f"Monitor Input: {monitor_output}")
    manifest = runner.process_monitoring_output(monitor_output, dry_run=dry_run)

    console.print("\n[bold green]Refresh Manifest:[/bold green]")
    console.print(f"Detected Issues: {len(manifest.detected_problems)}")
    if manifest.chosen_plan:
        console.print(f"Chosen Action Plan Risk: {manifest.chosen_plan.risk_level.value}")
        if manifest.chosen_plan.risk_level.value == "high":
            console.print(f"Manual Review Required Count: {len(manifest.chosen_plan.blocked_reasons)}")
        else:
             console.print(f"Auto-executed Action Count: {len(manifest.attempt.executed_actions) if manifest.attempt else 0}")

    console.print(f"Current Controller State: {manifest.current_state.value}")
    console.print(f"Freeze Active: {manifest.freeze_record is not None}")
    console.print(f"Degrade Active: {manifest.degrade_record is not None}")

    if manifest.attempt:
         console.print(f"Post-Refresh Validation Result: {'Passed' if manifest.attempt.validation_passed else 'Failed'}")

    console.print("\n[dim]Manifest output saved to artifact path (mocked)[/dim]")


@app.command("preview-refresh-plan")
def preview_refresh_plan(
    sport: str = typer.Option(..., help="Target sport"),
    market: str = typer.Option(..., help="Target market")
):
    """Preview a refresh plan for a given configuration without executing it."""
    run_refresh_controller(sport=sport, market=market, dry_run=True)

@app.command("preview-freeze-state")
def preview_freeze_state(
    sport: str = typer.Option(..., help="Target sport"),
    market: str = typer.Option(..., help="Target market")
):
    """Preview what the freeze state would look like for a given configuration."""
    console.print(f"[bold yellow]Previewing Freeze State[/bold yellow] for {sport}/{market}")
    # Force a freeze manually
    runner = RefreshControllerRunner()
    record = runner.freeze_mgr.activate_freeze("Preview requested")
    console.print(f"Freeze Reason: {record.freeze_reason}")
    console.print(f"Scope: {record.freeze_scope}")

@app.command("preview-degrade-state")
def preview_degrade_state(
    sport: str = typer.Option(..., help="Target sport"),
    market: str = typer.Option(..., help="Target market")
):
    """Preview what the degrade state would look like for a given configuration."""
    console.print(f"[bold yellow]Previewing Degrade State[/bold yellow] for {sport}/{market}")
    runner = RefreshControllerRunner()
    record = runner.degrade_mgr.activate_degrade("moderate", "Preview requested")
    console.print(f"Degrade Level: {record.degrade_level}")
    console.print(f"Reason: {record.reason}")

@app.command("list-refresh-actions")
def list_refresh_actions():
    """List all available refresh actions and their risk levels."""
    from .refresh_controller.states import RefreshActionFamily
    console.print("[bold]Available Refresh Actions:[/bold]")
    for action in RefreshActionFamily:
        console.print(f"- {action.value}")

if __name__ == "__main__":
    app()
