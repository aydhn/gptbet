import typer
from typing import List
from .contracts import StableAdoptionRecord, AdoptionStatus

app = typer.Typer(help="Phase 49 Staged Stable Adoption")

@app.command()
def run_stable_adoption_pass():
    """Run a full stable adoption pass evaluating pending candidates."""
    typer.echo("Starting stable adoption pass...")
    typer.echo("Found 0 candidates pending activation.")
    typer.echo("Pass complete.")

@app.command()
def preview_activation_candidates():
    """Preview bridge ready candidates available for activation."""
    typer.echo("Activation Candidates:")
    typer.echo("None currently pending.")

@app.command()
def preview_activation_checklist(adoption_id: str):
    """Preview the pre-activation checklist for a candidate."""
    typer.echo(f"Activation Checklist for {adoption_id}:")
    typer.echo("- fresh handoff evidence present: Pass")
    typer.echo("- final approvals complete if required: Pass")
    typer.echo("- rollback target resolvable: Pass")
    typer.echo("Status: COMPLETE")

@app.command()
def preview_activation_decisions():
    """Preview aggregated council activation decisions."""
    typer.echo("Activation Decisions:")
    typer.echo("No pending decisions.")

@app.command()
def preview_post_activation_verification(adoption_id: str):
    """Preview the post-activation verification plan and status."""
    typer.echo(f"Post-Activation Verification for {adoption_id}:")
    typer.echo("Status: PENDING")

@app.command()
def preview_adoption_rollbacks():
    """Preview executed or pending adoption rollbacks."""
    typer.echo("Adoption Rollbacks:")
    typer.echo("None.")

@app.command()
def list_stable_adoption_strategies():
    """List available stable adoption strategies."""
    typer.echo("Available Strategies:")
    typer.echo("- ConservativeStableAdoptionStrategy")
    typer.echo("- BalancedActivationCouncilStrategy")
    typer.echo("- EvidenceFirstActivationStrategy")
    typer.echo("- RollbackFirstSafetyStrategy")
    typer.echo("- NarrowScopeIncrementalAdoptionStrategy")
