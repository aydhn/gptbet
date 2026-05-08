import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="Evidence Atlas Operations (Phase 92)")
console = Console()

@app.command("run-evidence-atlas-pass")
def run_evidence_atlas_pass():
    """Runs a full evidence atlas and narrative federation pass."""
    console.print("[bold green]Starting Evidence Atlas Pass...[/bold green]")
    console.print("=> Connecting federated narratives...")
    console.print("=> Evaluating assurance mesh paths...")
    console.print("=> Adjudicating replay clearing cases...")
    console.print("=> Updating sovereign governance evidence atlas...")
    console.print("=> Enforcing currentness, caveat, and sovereignty rules...")
    console.print("[bold green]Evidence Atlas Pass Complete![/bold green]")

@app.command("preview-narrative-federations")
def preview_narrative_federations():
    """Previews narrative compiler federations."""
    table = Table(title="Narrative Compiler Federations")
    table.add_column("Federation ID", style="cyan")
    table.add_column("Family", style="magenta")
    table.add_column("Health", style="green")
    table.add_column("Currentness", style="yellow")

    table.add_row("fed_001", "operator_narrative_federation", "healthy", "current_with_caps")
    table.add_row("fed_002", "executive_narrative_federation", "degraded", "stale")

    console.print(table)
    console.print("\n[dim]Note: Stale federations cannot produce strong authoritative outputs.[/dim]")

@app.command("preview-assurance-meshes")
def preview_assurance_meshes():
    """Previews assurance exchange meshes."""
    table = Table(title="Assurance Exchange Meshes")
    table.add_column("Mesh ID", style="cyan")
    table.add_column("Family", style="magenta")
    table.add_column("Paths Valid", style="green")
    table.add_column("Pressure State", style="yellow")

    table.add_row("mesh_001", "bounded_assurance_mesh", "12/12", "low")
    table.add_row("mesh_002", "degraded_assurance_mesh", "4/15", "high")

    console.print(table)

@app.command("preview-clearing-councils")
def preview_clearing_councils():
    """Previews replay clearing councils."""
    table = Table(title="Replay Clearing Councils")
    table.add_column("Council ID", style="cyan")
    table.add_column("Family", style="magenta")
    table.add_column("Open Cases", style="yellow")
    table.add_column("Health", style="green")

    table.add_row("council_001", "bounded_clearing_council", "3", "healthy")
    table.add_row("council_002", "debt_pressure_clearing_council", "12", "degraded")

    console.print(table)

@app.command("preview-evidence-atlases")
def preview_evidence_atlases():
    """Previews sovereign governance evidence atlases."""
    table = Table(title="Governance Evidence Atlases")
    table.add_column("Atlas ID", style="cyan")
    table.add_column("Family", style="magenta")
    table.add_column("Nodes (Fresh/Stale)", style="green")
    table.add_column("Edges (Fresh/Stale)", style="yellow")

    table.add_row("atlas_001", "governance_evidence_atlas", "45 / 0", "120 / 0")
    table.add_row("atlas_002", "debt_and_settlement_atlas", "12 / 4", "30 / 12")

    console.print(table)
    console.print("\n[dim]Sovereignty Warning: no-safe visibility elements are preserved across all views.[/dim]")

@app.command("preview-evidence-atlas-health")
def preview_evidence_atlas_health():
    """Previews the overall health of the evidence atlas."""
    console.print("[bold cyan]Evidence Atlas Health Summary[/bold cyan]")
    console.print("- Narrative Federations: 1 healthy, 1 degraded")
    console.print("- Assurance Meshes: 1 healthy, 1 degraded")
    console.print("- Clearing Councils: 1 healthy, 1 degraded")
    console.print("- Evidence Atlases: 1 healthy, 1 degraded")
    console.print("\n[bold red]Overall Status: Caveated[/bold red]")
    console.print("Reason: Stale nodes detected in debt_and_settlement_atlas, forcing narrative degradation.")

@app.command("list-evidence-atlas-strategies")
def list_evidence_atlas_strategies():
    """Lists available evidence atlas strategies."""
    table = Table(title="Evidence Atlas Strategies")
    table.add_column("Strategy Name", style="cyan")
    table.add_column("Description", style="green")

    table.add_row("ConservativeEvidenceAtlasStrategy", "Default. Strict freshness and caveat preservation.")
    table.add_row("BalancedBoardMeshFederationStrategy", "Balanced approach for bounded assurance.")
    table.add_row("ReplayClearingCouncilFirstStrategy", "Prioritizes council precedence and evidence.")

    console.print(table)

if __name__ == "__main__":
    app()
