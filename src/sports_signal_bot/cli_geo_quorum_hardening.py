import typer
from rich.console import Console
from rich.panel import Panel
from rich.json import JSON
import json
import os
from src.sports_signal_bot.geo_quorum_hardening.integration import run_hardening_pass

app = typer.Typer(help="Geo Quorum Hardening (Pack 10) Operations")
console = Console()

@app.command("run-hardening-pack-10")
def run_hardening_pack_10(strategy: str = "conservative"):
    console.print(Panel(f"Running Geo Quorum Hardening (Pack 10) using strategy '{strategy}'", style="bold green"))
    manifest = run_hardening_pass(strategy)
    console.print("✅ Regional Quorum Drills Completed")
    console.print("✅ Active-Passive Rehearsals Completed")
    console.print("✅ Global Operator Coverage Synthesis Completed")
    console.print("✅ Rolling Evacuation Audit Chains Completed")
    console.print("✅ Artifacts saved to out/geo_quorum_hardening/")
    console.print(Panel(JSON(json.dumps(manifest, default=str)), title="Resulting Manifest", style="green"))

@app.command("preview-regional-quorum-report")
def preview_regional_quorum_report():
    filepath = "out/geo_quorum_hardening/regional_quorum_drills.json"
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            data = json.load(f)
        console.print(Panel(JSON(json.dumps(data)), title="Regional Quorum Report", style="cyan"))
    else:
        console.print("Run 'run-hardening-pack-10' first to generate report.")

@app.command("preview-active-passive-report")
def preview_active_passive_report():
    filepath = "out/geo_quorum_hardening/active_passive_rehearsals.json"
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            data = json.load(f)
        console.print(Panel(JSON(json.dumps(data)), title="Active-Passive Report", style="cyan"))
    else:
        console.print("Run 'run-hardening-pack-10' first to generate report.")

@app.command("preview-global-coverage-report")
def preview_global_coverage_report():
    filepath = "out/geo_quorum_hardening/global_operator_coverage_synthesis.json"
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            data = json.load(f)
        console.print(Panel(JSON(json.dumps(data)), title="Global Coverage Report", style="cyan"))
    else:
        console.print("Run 'run-hardening-pack-10' first to generate report.")

@app.command("preview-rolling-evacuation-report")
def preview_rolling_evacuation_report():
    filepath = "out/geo_quorum_hardening/rolling_evacuation_audit_chains.json"
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            data = json.load(f)
        console.print(Panel(JSON(json.dumps(data)), title="Rolling Evacuation Report", style="cyan"))
    else:
        console.print("Run 'run-hardening-pack-10' first to generate report.")

@app.command("preview-geo-quorum-hardening-health")
def preview_geo_quorum_hardening_health():
    filepath = "out/geo_quorum_hardening/geo_quorum_hardening_health_report.json"
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            data = json.load(f)
        console.print(Panel(JSON(json.dumps(data)), title="Geo Quorum Hardening Health", style="green"))
    else:
        console.print("Run 'run-hardening-pack-10' first to generate report.")

@app.command("list-geo-quorum-hardening-strategies")
def list_strategies():
    strategies = [
        "ConservativeGeoQuorumHardeningStrategy (conservative)",
        "BalancedGeoQuorumReadinessStrategy (balanced)",
        "QuorumIntegrityFirstStrategy (quorum_integrity_first)",
        "EvacuationChainFirstStrategy (evacuation_chain_first)"
    ]
    for s in strategies:
        console.print(f"- {s}")

if __name__ == "__main__":
    app()
