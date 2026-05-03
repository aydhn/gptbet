import typer
from rich.console import Console
from rich.table import Table
from .pass_runner import run_sample_scenarios

remediation_lanes_app = typer.Typer(help="Remediation Lane Architecture and Execution Governance CLI")
console = Console()

@remediation_lanes_app.command("run-remediation-lanes-pass")
def run_remediation_lanes_pass():
    """Runs the full lifecycle pass for remediation lanes, tokens, readiness, and closure."""
    console.print("[bold cyan]Starting Phase 71 Remediation Lanes Pass...[/bold cyan]")
    manifest = run_sample_scenarios()

    console.print(f"[green]✔ Pass completed. Manifest ID: {manifest.manifest_id}[/green]")
    console.print("\n[bold]Summary:[/bold]")
    for k, v in manifest.summary.items():
        console.print(f"  - {k}: {v}")

    console.print("\n[dim]Artifact saved to: remediation_lanes_manifest.json[/dim]")

@remediation_lanes_app.command("preview-remediation-lanes")
def preview_remediation_lanes():
    """Shows defined remediation lanes and their eligibility status."""
    manifest = run_sample_scenarios()
    table = Table(title="Remediation Lanes")
    table.add_column("Lane ID")
    table.add_column("Family")
    table.add_column("Status")
    table.add_column("Rollback Verified")

    for lane in manifest.active_lanes:
        table.add_row(lane.lane_id, lane.lane_family.value, lane.current_status.value, str(lane.rollback_binding.is_verified_in_rehearsal))
    console.print(table)

@remediation_lanes_app.command("preview-execution-tokens")
def preview_execution_tokens():
    """Previews currently issued bounded execution tokens."""
    manifest = run_sample_scenarios()
    table = Table(title="Bounded Execution Tokens")
    table.add_column("Token ID")
    table.add_column("Lane Ref")
    table.add_column("Status")
    table.add_column("Expiry")

    for token in manifest.active_tokens:
        table.add_row(token.token_id, token.bound_lane_ref, token.status, str(token.valid_until))
    console.print(table)

@remediation_lanes_app.command("preview-loop-closure-records")
def preview_loop_closure_records():
    """Shows loop closure verification results for executed lanes."""
    manifest = run_sample_scenarios()
    table = Table(title="Loop Closure Verification")
    table.add_column("Lane Ref")
    table.add_column("Outcome")
    table.add_column("Checkpoints Met")
    table.add_column("Rollback Used")

    for closure in manifest.closures:
        table.add_row(closure.lane_ref, closure.outcome.value, str(closure.checkpoints_met), str(closure.rollback_used))
    console.print(table)

@remediation_lanes_app.command("preview-federated-playbook-catalogs")
def preview_federated_playbook_catalogs():
    """Previews discoverable federated playbook listings."""
    manifest = run_sample_scenarios()
    table = Table(title="Federated Playbook Exchange Catalog")
    table.add_column("Catalog ID")
    table.add_column("Listing Count")
    table.add_column("Health")

    for cat in manifest.catalogs:
        table.add_row(cat.catalog_id, str(len(cat.listings)), cat.catalog_health)
    console.print(table)

@remediation_lanes_app.command("list-remediation-lane-strategies")
def list_remediation_lane_strategies():
    """Lists available remediation lane strategies."""
    strats = [
        "ConservativeLaneExecutionStrategy",
        "BalancedReviewAwareLaneStrategy",
        "FederatedCatalogAwareLaneStrategy",
        "ClosureFirstStrategy",
        "TokenStrictStrategy"
    ]
    console.print("[bold]Available Strategies:[/bold]")
    for s in strats:
        console.print(f" - [cyan]{s}[/cyan]")
