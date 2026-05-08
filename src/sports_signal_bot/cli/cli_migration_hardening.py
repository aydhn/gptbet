import typer
from rich.console import Console
from sports_signal_bot.migration_hardening.integration import MigrationHardeningOrchestrator
from sports_signal_bot.migration_hardening.manifests import generate_migration_hardening_manifest
import json
import os

app = typer.Typer()
console = Console()

@app.command("run-hardening-pack-07")
def run_hardening_pack_07():
    console.print("[bold green]Running Post-100 Hardening Pack 07: Disaster Migration & Coordination...[/bold green]")
    orchestrator = MigrationHardeningOrchestrator()
    orchestrator.run_all_simulations()

    summary = orchestrator.get_summary()
    manifest = generate_migration_hardening_manifest(summary)

    # Write artifacts
    os.makedirs("artifacts/migration_hardening", exist_ok=True)

    with open("artifacts/migration_hardening/disaster_migration_lanes.json", "w") as f:
        json.dump(summary.get("migration_lanes", []), f, indent=2)
    with open("artifacts/migration_hardening/multi_team_coordination_drills.json", "w") as f:
        json.dump(summary.get("coordination_drills", []), f, indent=2)
    with open("artifacts/migration_hardening/archival_recovery_chains.json", "w") as f:
        json.dump(summary.get("recovery_chains", []), f, indent=2)
    with open("artifacts/migration_hardening/governance_visibility_wargames.json", "w") as f:
        json.dump(summary.get("visibility_wargames", []), f, indent=2)
    with open("artifacts/migration_hardening/coordination_handoff_report.json", "w") as f:
        json.dump({"note": "Detailed handoff report simulated"}, f, indent=2)
    with open("artifacts/migration_hardening/recovery_chain_restore_report.json", "w") as f:
        json.dump({"note": "Detailed chain restore report simulated"}, f, indent=2)
    with open("artifacts/migration_hardening/operational_resilience_budgets.json", "w") as f:
        json.dump({"note": "Budgets report simulated"}, f, indent=2)
    with open("artifacts/migration_hardening/operational_visibility_matrix.json", "w") as f:
        json.dump(summary.get("visibility_matrix", {}), f, indent=2)
    with open("artifacts/migration_hardening/migration_hardening_health_report.json", "w") as f:
        json.dump(summary, f, indent=2)
    with open("artifacts/migration_hardening/migration_hardening_manifest.json", "w") as f:
        f.write(manifest)

    console.print(f"Overall Health: [bold]{summary['overall_health']}[/bold]")
    console.print(f"Release Blockers: {summary['release_blockers']}")
    console.print("Artifacts generated in artifacts/migration_hardening/")

@app.command("preview-migration-lane-report")
def preview_migration_lane_report():
    orchestrator = MigrationHardeningOrchestrator()
    orchestrator.simulate_archive_to_runtime_migration()
    summary = orchestrator.get_summary()
    console.print(json.dumps(summary["migration_lanes"], indent=2))

@app.command("preview-team-coordination-report")
def preview_team_coordination_report():
    orchestrator = MigrationHardeningOrchestrator()
    orchestrator.simulate_cross_team_no_safe_handoff()
    summary = orchestrator.get_summary()
    console.print(json.dumps(summary["coordination_drills"], indent=2))

@app.command("preview-recovery-chain-report")
def preview_recovery_chain_report():
    orchestrator = MigrationHardeningOrchestrator()
    orchestrator.simulate_broken_recovery_chain()
    summary = orchestrator.get_summary()
    console.print(json.dumps(summary["recovery_chains"], indent=2))

@app.command("preview-visibility-wargame-report")
def preview_visibility_wargame_report():
    orchestrator = MigrationHardeningOrchestrator()
    orchestrator.simulate_executive_visibility_honesty()
    summary = orchestrator.get_summary()
    console.print(json.dumps(summary["visibility_wargames"], indent=2))

@app.command("preview-migration-hardening-health")
def preview_migration_hardening_health():
    orchestrator = MigrationHardeningOrchestrator()
    orchestrator.run_all_simulations()
    summary = orchestrator.get_summary()
    console.print(json.dumps(summary, indent=2))

@app.command("list-migration-hardening-strategies")
def list_migration_hardening_strategies():
    strategies = [
        "ConservativeMigrationHardeningStrategy",
        "BalancedMigrationReadinessStrategy",
        "ChainIntegrityFirstStrategy",
        "VisibilityWarGameFirstStrategy"
    ]
    for s in strategies:
        console.print(f"- {s}")

if __name__ == "__main__":
    app()
