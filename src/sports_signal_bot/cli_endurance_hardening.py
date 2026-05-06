import typer
from rich.console import Console
from sports_signal_bot.endurance_hardening.integration import run_endurance_hardening_pack
from sports_signal_bot.endurance_hardening.utils import format_endurance_output
from sports_signal_bot.endurance_hardening.strategies import (
    ConservativeEnduranceHardeningStrategy,
    BalancedEnduranceReadinessStrategy,
    ArchivalIntegrityFirstStrategy,
    RunbookSafetyFirstStrategy
)

app = typer.Typer()
console = Console()

@app.command("run-hardening-pack-05")
def run_hardening_pack_05():
    """Runs the Post-100 Hardening Pack 05 (Endurance Hardening)."""
    console.print("Running Post-100 Hardening Pack 05...")
    results = run_endurance_hardening_pack()
    console.print(format_endurance_output(results["summary"]))

@app.command("preview-soak-report")
def preview_soak_report():
    """Previews the soak endurance report."""
    results = run_endurance_hardening_pack()
    console.print(format_endurance_output(results["results"]["soak"]))

@app.command("preview-drift-report")
def preview_drift_report():
    """Previews the long-horizon drift report."""
    results = run_endurance_hardening_pack()
    console.print(format_endurance_output(results["results"]["drift"]))

@app.command("preview-archival-integrity-report")
def preview_archival_integrity_report():
    """Previews the archival integrity report."""
    results = run_endurance_hardening_pack()
    console.print(format_endurance_output(results["results"]["archive"]))

@app.command("preview-runbook-verification-report")
def preview_runbook_verification_report():
    """Previews the runbook verification report."""
    results = run_endurance_hardening_pack()
    console.print(format_endurance_output(results["results"]["runbook"]))

@app.command("preview-residue-accumulation-report")
def preview_residue_accumulation_report():
    """Previews the residue accumulation report."""
    console.print(format_endurance_output({"residue_report": "simulated_data"}))

@app.command("preview-endurance-hardening-health")
def preview_endurance_hardening_health():
    """Previews the overall endurance hardening health report."""
    results = run_endurance_hardening_pack()
    console.print(format_endurance_output(results["summary"]))

@app.command("list-endurance-hardening-strategies")
def list_endurance_hardening_strategies():
    """Lists the available endurance hardening strategies."""
    strategies = [
        ConservativeEnduranceHardeningStrategy().strategy_name,
        BalancedEnduranceReadinessStrategy().strategy_name,
        ArchivalIntegrityFirstStrategy().strategy_name,
        RunbookSafetyFirstStrategy().strategy_name
    ]
    console.print(format_endurance_output({"strategies": strategies}))
