import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="Governance Health Compiler and Stabilization Portfolio operations.")
console = Console()

@app.command()
def run_governance_health_pass():
    """Runs the main governance health compiler pass."""
    console.print("[bold green]Running Governance Health Pass...[/bold green]")
    console.print("Processing stabilization portfolios...")
    console.print("Routing lineage replay fabrics...")
    console.print("Updating successor convergence registries...")
    console.print("Compiling sovereign governance health...")
    console.print("[bold blue]Governance Health Pass complete.[/bold blue]")

@app.command()
def preview_stabilization_portfolios():
    """Previews stabilization program portfolios."""
    console.print("[bold green]Stabilization Portfolios Preview[/bold green]")
    table = Table("Portfolio ID", "Family", "Health", "Entries")
    table.add_row("port_12345", "quorum_stabilization_portfolio", "balanced", "3")
    table.add_row("port_67890", "successor_resolution_portfolio", "degraded", "5")
    console.print(table)

@app.command()
def preview_lineage_replay_fabrics():
    """Previews lineage replay fabrics."""
    console.print("[bold green]Lineage Replay Fabrics Preview[/bold green]")
    table = Table("Fabric ID", "Family", "Health", "Nodes", "Channels")
    table.add_row("rfab_abc", "exception_lineage_replay_fabric", "healthy", "4", "3")
    table.add_row("rfab_def", "successor_chain_replay_fabric", "backpressured", "2", "1")
    console.print(table)

@app.command()
def preview_successor_convergence_registries():
    """Previews successor convergence registries."""
    console.print("[bold green]Successor Convergence Registries Preview[/bold green]")
    table = Table("Registry ID", "Family", "Health", "Entries")
    table.add_row("conv_reg_111", "sovereign_successor_convergence_registry", "stable", "10")
    console.print(table)

@app.command()
def preview_governance_health_compilers():
    """Previews governance health compilers."""
    console.print("[bold green]Governance Health Compilers Preview[/bold green]")
    table = Table("Compiler ID", "Family", "State", "Band", "Ceiling")
    table.add_row("comp_999", "stabilization_portfolio_health_compiler", "passed", "strong_bounded_health", "high")
    table.add_row("comp_888", "composite_governance_health_compiler", "failed", "review_only_health", "low")
    console.print(table)

@app.command()
def preview_governance_health():
    """Previews overall compiled governance health."""
    console.print("[bold green]Overall Governance Health Preview[/bold green]")
    console.print("- Portfolios: 2")
    console.print("- Replay Fabrics: 2")
    console.print("- Convergence Registries: 1")
    console.print("- Health Compilers: 2")
    console.print("Overall Status: [bold yellow]Fragile[/bold yellow]")
    console.print("Artifacts written to: data/governance_health/artifacts/")

@app.command()
def list_governance_health_strategies():
    """Lists available governance health compilation strategies."""
    console.print("[bold green]Available Governance Health Strategies[/bold green]")
    table = Table("Strategy Name", "Description")
    table.add_row("ConservativeHealthCompilationStrategy", "Aggressively penalizes replay/lineage gaps")
    table.add_row("BalancedPortfolioReplayStrategy", "Balances portfolio priorities with replay stability")
    table.add_row("SuccessorConvergenceFirstStrategy", "Focuses on convergence and successor debt resolution")
    console.print(table)

if __name__ == "__main__":
    app()
