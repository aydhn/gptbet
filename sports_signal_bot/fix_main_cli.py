import re

with open("src/sports_signal_bot/main_cli.py", "r") as f:
    content = f.read()

commands = """
# =====================================================================
# Monitoring Commands
# =====================================================================

@app.command(name="run-monitoring", help="Run monitoring health checks and output artifacts")
def run_monitoring(
    sport: str = typer.Argument(..., help="Target sport"),
    market: str = typer.Argument("all", help="Target market"),
    slot: str = typer.Option("midday", help="Time slot"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Run without sending dispatches or writing artifacts")
):
    from sports_signal_bot.monitoring.runner import MonitoringRunner
    from datetime import datetime

    run_id = f"{sport}_{market}_{slot}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
    results_dir = f"results/{sport}_{market}"

    runner = MonitoringRunner(run_id=run_id, results_dir=results_dir, dry_run=dry_run)
    manifest = runner.run(sport, market)

    typer.echo(f"Monitoring Run ID: {run_id}")
    if manifest.health_score:
        typer.echo(f"Global Health Score: {manifest.health_score.global_score:.1f}/100.0 [{manifest.health_score.global_status.value}]")
    typer.echo(f"Anomalies detected: {manifest.total_anomalies}")
    if manifest.escalation_summary:
        typer.echo(f"Escalations: {manifest.escalation_summary.alerts_escalated}")

@app.command(name="preview-health-score", help="Preview health score for a given run without writing artifacts")
def preview_health_score(
    sport: str = typer.Argument(..., help="Target sport"),
    market: str = typer.Argument("all", help="Target market"),
):
    run_monitoring(sport=sport, market=market, dry_run=True)

@app.command(name="preview-anomalies", help="Preview anomalies for a given run without writing artifacts")
def preview_anomalies(
    sport: str = typer.Argument(..., help="Target sport"),
    market: str = typer.Argument("all", help="Target market"),
):
    run_monitoring(sport=sport, market=market, dry_run=True)

@app.command(name="preview-heartbeat", help="Preview heartbeat for a given run without writing artifacts")
def preview_heartbeat(
    sport: str = typer.Argument(..., help="Target sport"),
    market: str = typer.Argument("all", help="Target market"),
):
    run_monitoring(sport=sport, market=market, dry_run=True)

@app.command(name="list-health-checks", help="List all registered health checks")
def list_health_checks():
    from sports_signal_bot.monitoring.registry import HealthCheckRegistry
    # Ensure components are loaded to register checks
    import sports_signal_bot.monitoring.components.data
    import sports_signal_bot.monitoring.components.artifacts
    import sports_signal_bot.monitoring.components.inference
    import sports_signal_bot.monitoring.components.outputs
    import sports_signal_bot.monitoring.components.dispatch
    import sports_signal_bot.monitoring.components.portfolio
    import sports_signal_bot.monitoring.components.bankroll

    components = HealthCheckRegistry.get_all_components()
    for comp in components:
        checks = HealthCheckRegistry.get_checks(comp)
        typer.echo(f"Component: {comp}")
        for check in checks:
            typer.echo(f"  - {check.__name__}")
"""

# Try to insert before portfolio_app
insert_index = content.find("from sports_signal_bot.portfolio import portfolio_app")
if insert_index == -1:
    # Try before __main__
    insert_index = content.find("if __name__ == ")

if insert_index != -1:
    final_content = content[:insert_index] + commands + "\n\n" + content[insert_index:]
    with open("src/sports_signal_bot/main_cli.py", "w") as f:
        f.write(final_content)
    print("Added commands to main_cli.py")
else:
    print("Could not find insertion point")
