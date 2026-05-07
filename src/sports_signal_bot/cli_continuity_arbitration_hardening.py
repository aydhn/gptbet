import typer
import json
from src.sports_signal_bot.continuity_arbitration_hardening.integration import run_continuity_arbitration_hardening_pass

app = typer.Typer()

@app.command("run-hardening-pack-18")
def run_hardening_pack_18():
    """Run Post-100 Hardening Pack 18 operations."""
    typer.echo("Running Continuity Arbitration Hardening Pass...")
    report = run_continuity_arbitration_hardening_pass()
    typer.echo(json.dumps(report, indent=2))
    typer.echo("Hardening pass complete. Artifacts generated.")

@app.command("preview-continuity-arbitration-rail-report")
def preview_rail_report():
    report = run_continuity_arbitration_hardening_pass()
    typer.echo(json.dumps(report["continuity_arbitration_rails"], indent=2))

@app.command("preview-scheduler-recovery-fabric-report")
def preview_fabric_report():
    report = run_continuity_arbitration_hardening_pass()
    typer.echo(json.dumps(report["scheduler_recovery_fabrics"], indent=2))

@app.command("preview-archive-proof-mesh-report")
def preview_mesh_report():
    report = run_continuity_arbitration_hardening_pass()
    typer.echo(json.dumps(report["archive_proof_meshes"], indent=2))

@app.command("preview-worldwide-visibility-ledger-report")
def preview_ledger_report():
    report = run_continuity_arbitration_hardening_pass()
    typer.echo(json.dumps(report["worldwide_visibility_ledgers"], indent=2))

@app.command("preview-continuity-arbitration-health")
def preview_health():
    report = run_continuity_arbitration_hardening_pass()

    rail_caveated = sum(1 for r in report["continuity_arbitration_rails"] if r["status"] != "rail_verified")
    fabric_caveated = sum(1 for r in report["scheduler_recovery_fabrics"] if r["status"] != "fabric_verified")
    mesh_broken = sum(1 for r in report["archive_proof_meshes"] if r["status"] != "mesh_verified")
    ledger_caveated = sum(1 for r in report["worldwide_visibility_ledgers"] if r["status"] != "ledger_verified")

    summary = {
        "rail_caveated_counts": rail_caveated,
        "fabric_caveated_counts": fabric_caveated,
        "mesh_broken_counts": mesh_broken,
        "ledger_caveated_counts": ledger_caveated,
        "overall_status": "caveated" if any([rail_caveated, fabric_caveated, mesh_broken, ledger_caveated]) else "verified"
    }
    typer.echo(json.dumps(summary, indent=2))

@app.command("list-continuity-arbitration-strategies")
def list_strategies():
    strategies = [
        "ConservativeContinuityArbitrationStrategy",
        "BalancedArbitrationReadinessStrategy",
        "ProofMeshFirstStrategy",
        "VisibilityLedgerFirstStrategy"
    ]
    for s in strategies:
        typer.echo(f"- {s}")

if __name__ == "__main__":
    app()
