import typer
from sports_signal_bot.planetary_federation_hardening.integration import run_hardening_pack_15
import json
import os

app = typer.Typer(help="Planetary Federation Hardening CLI")

@app.command()
def run_hardening_pack_15_command():
    """Run Planetary Federation Hardening Pack 15"""
    typer.echo("Running Planetary Federation Hardening Pack 15...")
    run_hardening_pack_15()
    typer.echo("Done.")

@app.command()
def preview_planetary_mesh_federation_report():
    """Preview planetary mesh federation report"""
    try:
        with open("artifacts/planetary_mesh_federations.json") as f:
            data = json.load(f)
            typer.echo(json.dumps(data, indent=2))
    except FileNotFoundError:
        typer.echo("No report found. Run hardening pack 15 first.")

@app.command()
def preview_corridor_superchain_report():
    """Preview corridor superchain report"""
    try:
        with open("artifacts/corridor_superchains.json") as f:
            data = json.load(f)
            typer.echo(json.dumps(data, indent=2))
    except FileNotFoundError:
        typer.echo("No report found. Run hardening pack 15 first.")

@app.command()
def preview_scheduler_bus_report():
    """Preview scheduler bus report"""
    try:
        with open("artifacts/scheduler_buses.json") as f:
            data = json.load(f)
            typer.echo(json.dumps(data, indent=2))
    except FileNotFoundError:
        typer.echo("No report found. Run hardening pack 15 first.")

@app.command()
def preview_audit_cadence_report():
    """Preview global audit cadence orchestration report"""
    try:
        with open("artifacts/global_audit_cadence_orchestration.json") as f:
            data = json.load(f)
            typer.echo(json.dumps(data, indent=2))
    except FileNotFoundError:
        typer.echo("No report found. Run hardening pack 15 first.")

@app.command()
def preview_planetary_federation_hardening_health():
    """Preview planetary federation hardening health"""
    try:
        with open("artifacts/planetary_federation_hardening_health_report.json") as f:
            data = json.load(f)
            typer.echo(json.dumps(data, indent=2))
    except FileNotFoundError:
        typer.echo("No report found. Run hardening pack 15 first.")

@app.command()
def list_planetary_federation_hardening_strategies():
    """List planetary federation hardening strategies"""
    typer.echo("Available strategies:")
    typer.echo("- ConservativePlanetaryFederationHardeningStrategy")
    typer.echo("- BalancedFederationReadinessStrategy")
    typer.echo("- SuperchainIntegrityFirstStrategy")
    typer.echo("- CadenceTruthFirstStrategy")

if __name__ == "__main__":
    app()
