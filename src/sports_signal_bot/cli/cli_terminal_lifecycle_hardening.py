import typer
import json
from .terminal_lifecycle_hardening.integration import TerminalLifecycleHardeningIntegrator

app = typer.Typer(help="Post-100 Hardening Pack 21: Terminal Lifecycle Hardening")

@app.command("run-hardening-pack-21")
def run_hardening_pack_21():
    typer.echo("Running Hardening Pack 21: Terminal Lifecycle Hardening")
    integrator = TerminalLifecycleHardeningIntegrator()
    integrator.run_pass()
    summary = integrator.summarize()

    with open("closure_bundles.json", "w") as f:
        json.dump(summary["closure_bundles"], f, indent=2)
    with open("deprecation_maps.json", "w") as f:
        json.dump(summary["deprecation_maps"], f, indent=2)
    with open("maintenance_modes.json", "w") as f:
        json.dump(summary["maintenance_modes"], f, indent=2)
    with open("long_horizon_stewardship_packs.json", "w") as f:
        json.dump(summary["stewardship_packs"], f, indent=2)
    with open("terminal_lifecycle_matrix.json", "w") as f:
        json.dump({"matrix_rows": summary["matrix_rows"]}, f, indent=2)
    with open("terminal_lifecycle_health_report.json", "w") as f:
        json.dump({"health": summary["health"]}, f, indent=2)
    with open("terminal_lifecycle_manifest.json", "w") as f:
        json.dump({"manifest_id": "terminal_manifest_1"}, f, indent=2)

    typer.echo("Hardening Pack 21 run complete. Artifacts generated.")

@app.command("preview-closure-bundle-report")
def preview_closure_bundle_report():
    integrator = TerminalLifecycleHardeningIntegrator()
    integrator.run_pass()
    typer.echo(json.dumps(integrator.summarize()["closure_bundles"], indent=2))

@app.command("preview-deprecation-map-report")
def preview_deprecation_map_report():
    integrator = TerminalLifecycleHardeningIntegrator()
    integrator.run_pass()
    typer.echo(json.dumps(integrator.summarize()["deprecation_maps"], indent=2))

@app.command("preview-maintenance-mode-report")
def preview_maintenance_mode_report():
    integrator = TerminalLifecycleHardeningIntegrator()
    integrator.run_pass()
    typer.echo(json.dumps(integrator.summarize()["maintenance_modes"], indent=2))

@app.command("preview-stewardship-pack-report")
def preview_stewardship_pack_report():
    integrator = TerminalLifecycleHardeningIntegrator()
    integrator.run_pass()
    typer.echo(json.dumps(integrator.summarize()["stewardship_packs"], indent=2))

@app.command("preview-terminal-lifecycle-health")
def preview_terminal_lifecycle_health():
    integrator = TerminalLifecycleHardeningIntegrator()
    integrator.run_pass()
    typer.echo(json.dumps({"health": integrator.summarize()["health"]}, indent=2))

@app.command("list-terminal-lifecycle-strategies")
def list_terminal_lifecycle_strategies():
    typer.echo("- ConservativeTerminalLifecycleStrategy")
    typer.echo("- BalancedTerminalLifecycleStrategy")
    typer.echo("- BaselineRetentionFirstStrategy")
    typer.echo("- StewardshipClarityFirstStrategy")

if __name__ == "__main__":
    app()
