import typer
import json
from rich.console import Console
from src.sports_signal_bot.trust_exchange_scale import run_trust_exchange_scale_pass

app = typer.Typer(help="Trust Exchange & Scale Architecture (Phase 81)")
console = Console()

@app.command("run-trust-exchange-scale-pass")
def run_pass():
    """Run a full trust exchange, scaled routing, and baseline governance pass."""
    result = run_trust_exchange_scale_pass()

    # Write artifacts (mock)
    import os
    os.makedirs("artifacts/trust_exchange", exist_ok=True)
    with open("artifacts/trust_exchange/trust_exchange_scale_summary.json", "w") as f:
        json.dump(result, f, indent=2, default=str)

    console.print("[bold green]Trust Exchange Scale Pass Complete[/bold green]")
    console.print(f"Overall Health: {result['overall_health']}")
    console.print(f"Overlay Packets: 1 ({result['overlay_exchange_packet']['exchange_status']})")
    console.print(f"Mesh Partitions: {len(result['scaled_mesh']['partition_refs'])}")
    console.print(f"Active Signals: {len(result['signal_ecosystem']['active_signal_refs'])}")
    console.print(f"Suppressed Signals: {len(result['signal_ecosystem']['suppression_refs'])}")
    console.print(f"Baselines: {len(result['baselines'])} (Drifted: {sum(1 for b in result['baselines'] if b['baseline_status'] == 'drifted')})")
    console.print(f"Controller Actions: {len(result['controller_actions'])}")
    console.print("Artifact written to: artifacts/trust_exchange/trust_exchange_scale_summary.json")

@app.command("preview-overlay-exchanges")
def preview_exchanges():
    console.print("[bold blue]Preview Overlay Exchanges[/bold blue]")
    console.print("- packet: oep-xxxx (validated) -> caveats preserved: ['default_caveat']")

@app.command("preview-scaled-hub-meshes")
def preview_meshes():
    console.print("[bold blue]Preview Scaled Hub Meshes[/bold blue]")
    console.print("- partition: part-bounded (low pressure)")
    console.print("- partition: part-review-only (high pressure) -> degradation active")

@app.command("preview-signal-ecologies")
def preview_signals():
    console.print("[bold blue]Preview Signal Ecologies[/bold blue]")
    console.print("- sig-1: healthy")
    console.print("- sig-2: stale -> SUPPRESSED")

@app.command("preview-governance-baselines")
def preview_baselines():
    console.print("[bold blue]Preview Governance Baselines[/bold blue]")
    console.print("- sovereignty_respect: aligned (drift 0.05)")
    console.print("- currentness_hygiene: drifted (drift 0.25)")

@app.command("list-trust-exchange-scale-strategies")
def list_strats():
    console.print("[bold blue]Available Strategies[/bold blue]")
    console.print("1. ConservativeOverlayExchangeStrategy (default)")
    console.print("2. BalancedScaledMeshStrategy")
    console.print("3. BaselineGovernanceFirstStrategy")

if __name__ == "__main__":
    app()
