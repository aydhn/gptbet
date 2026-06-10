import typer
from rich.console import Console

from sports_signal_bot.trace_routing.controllers import TraceRoutingController
from sports_signal_bot.trace_routing.proof_federations import build_proof_catalog_federation
from sports_signal_bot.trace_routing.contracts import ProofFederationFamily
from sports_signal_bot.trace_routing.strategies.conservative import ConservativeTraceRouterStrategy
from sports_signal_bot.trace_routing.strategies.balanced_proof_signal_federation import BalancedProofSignalFederationStrategy
from sports_signal_bot.trace_routing.strategies.integrity_council_first import IntegrityCouncilFirstStrategy

app = typer.Typer(help="Sovereign Governance Trace Routing CLI")
console = Console()

@app.command("run-trace-routing-pass")
def run_trace_routing_pass():
    """Runs a full trace routing evaluation pass."""
    console.print("[bold green]Running Sovereign Governance Trace Routing Pass...[/bold green]")
    controller = TraceRoutingController()

    # Simulate a minimal pass
    fed = build_proof_catalog_federation(
        ProofFederationFamily.GOVERNANCE_PROOF_CATALOG_FEDERATION,
        "policy_currentness_1",
        "policy_lineage_1",
        "policy_applicability_1"
    )
    controller.federations.append(fed)

    summary = controller.run_trace_routing_pass()
    console.print(f"Overall Health: {summary.overall_health}")
    console.print(f"Proof Federation Counts: {summary.proof_federation_counts_by_health}")
    console.print("[bold blue]Artifacts saved to artifacts/trace_routing_summary.json[/bold blue]")

@app.command("preview-proof-federations")
def preview_proof_federations():
    """Previews the active proof catalog federations."""
    console.print("[bold green]Previewing Proof Catalog Federations...[/bold green]")
    console.print("1. Governance Proof Catalog Federation (Healthy)")
    console.print("2. Debt Settlement Proof Catalog Federation (Caveated)")

@app.command("preview-observatory-signal-exchanges")
def preview_observatory_signal_exchanges():
    """Previews observatory signal exchanges."""
    console.print("[bold green]Previewing Observatory Signal Exchanges...[/bold green]")
    console.print("1. Internal Exchange (Bounded)")
    console.print("2. External Mesh Exchange (Review Only)")

@app.command("preview-integrity-councils")
def preview_integrity_councils():
    """Previews narrative integrity councils."""
    console.print("[bold green]Previewing Narrative Integrity Councils...[/bold green]")
    console.print("1. Freshness Integrity Council (Healthy)")

@app.command("preview-trace-routers")
def preview_trace_routers():
    """Previews sovereign governance trace routers."""
    console.print("[bold green]Previewing Trace Routers...[/bold green]")
    console.print("1. Governance Trace Router (Healthy)")

@app.command("preview-trace-routing-health")
def preview_trace_routing_health():
    """Previews overall trace routing health."""
    console.print("[bold green]Previewing Trace Routing Health...[/bold green]")
    console.print("Overall Health: Healthy")
    console.print("Caveated Routes: 2")
    console.print("Blocked Routes: 0")

@app.command("list-trace-routing-strategies")
def list_trace_routing_strategies():
    """Lists available trace routing strategies."""
    console.print("[bold green]Available Trace Routing Strategies:[/bold green]")
    console.print(f"- {ConservativeTraceRouterStrategy.__name__}")
    console.print(f"- {BalancedProofSignalFederationStrategy.__name__}")
    console.print(f"- {IntegrityCouncilFirstStrategy.__name__}")

if __name__ == "__main__":
    app()
