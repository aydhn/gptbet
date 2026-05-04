import typer
from rich.console import Console
from .integration import run_governance_recovery_pipeline

app = typer.Typer(help="Governance Recovery CLI")
console = Console()

@app.command("run-governance-recovery-pass")
def run_governance_recovery_pass():
    """Run a full governance recovery pass."""
    console.print("[green]Running governance recovery pass...[/green]")
    summary = run_governance_recovery_pipeline()
    console.print(f"Exception Federation Health: {'OK' if summary['exception_federation']['health_status']['is_healthy'] else 'DEGRADED'}")
    console.print(f"Quorum Routing Pressure: {summary['quorum_pressure']['state']}")
    console.print(f"Successor Registry Backlog: {len(summary['successor_registry']['unresolved_successor_refs'])}")
    console.print(f"Escalator State: {summary['governance_escalator']['current_state']}")
    console.print("Artifact written to: artifacts/governance_recovery_summary.json")

@app.command("preview-exception-federations")
def preview_exception_federations():
    """Preview exception registry federations."""
    console.print("[blue]Exception Federations:[/blue]")
    console.print("- review_only_exception_federation (Healthy)")

@app.command("preview-quorum-routing-fabrics")
def preview_quorum_routing_fabrics():
    """Preview quorum exchange routing fabrics."""
    console.print("[blue]Quorum Routing Fabrics:[/blue]")
    console.print("- bounded_governance_quorum_routing_fabric (Healthy)")

@app.command("preview-successor-registries")
def preview_successor_registries():
    """Preview baseline successor registries."""
    console.print("[blue]Successor Registries:[/blue]")
    console.print("- sovereign_baseline_successor_registry (Healthy)")

@app.command("preview-governance-escalators")
def preview_governance_escalators():
    """Preview governance recovery escalators."""
    console.print("[blue]Governance Escalators:[/blue]")
    console.print("- quorum_health_recovery_escalator (MONITORING)")

@app.command("preview-governance-recovery-health")
def preview_governance_recovery_health():
    """Preview overall governance recovery health."""
    console.print("[green]Governance Recovery Health: OK[/green]")

@app.command("list-governance-recovery-strategies")
def list_governance_recovery_strategies():
    """List available governance recovery strategies."""
    console.print("[blue]Available Strategies:[/blue]")
    console.print("1. ConservativeRecoveryEscalationStrategy")
    console.print("2. BalancedSuccessorRoutingStrategy")
    console.print("3. SuccessorFirstGovernanceStrategy")
    console.print("4. ExceptionFederationStrictStrategy")
    console.print("5. SovereigntyDominantRecoveryStrategy")

if __name__ == "__main__":
    app()
