from .staged_channels.cli import app as staged_channels_app
import typer
from .tournaments.cli import app as tournaments_app
from .candidate_promotion.cli import app as candidate_promotion_app
from .auto_promotion.cli import app as auto_promotion_app
from .deployment.cli import app as deployment_app
from .handoff.cli import app as handoff_app
import json
from datetime import datetime

# Import simulation components
from .simulation.contracts import SimulationRequestRecord, SimulationMode
from .simulation.patches import build_candidate_patch
from .simulation.strategies.balanced_comparative import BalancedComparativeStrategy

app = typer.Typer(help="Sports Signal Bot CLI")
app.add_typer(staged_channels_app, name="staged-channels", help="Phase 46 Staged Channels")

@app.command()
def simulate_suggestion(suggestion_id: str):
    """Run a sandbox simulation for a candidate patch suggestion."""
    typer.echo(f"Starting simulation for suggestion: {suggestion_id}")

    # Mock suggestion
    mock_suggestion = {
        "suggestion_id": suggestion_id,
        "target_component_family": "provider_priority",
        "patch_payload": {"priority": "high"},
        "scope": {"sport": "football"}
    }

    patch = build_candidate_patch(mock_suggestion)
    request = SimulationRequestRecord(
        request_id=f"req_{datetime.utcnow().timestamp()}",
        suggestion_ids=[suggestion_id],
        simulation_mode=SimulationMode.COMPARATIVE_SLOT_REPLAY,
        audience_profile="operator",
        replay_window={"start": datetime.utcnow(), "end": datetime.utcnow()}
    )

    strategy = BalancedComparativeStrategy()
    run_record = strategy.run_simulation(request, patch)

    typer.echo(f"\n--- Simulation Result ---")
    typer.echo(f"Run ID: {run_record.run_id}")
    typer.echo(f"Status: {run_record.status}")
    if run_record.comparison:
        typer.echo(f"Comparison Status: {run_record.comparison.status.value}")
        typer.echo(f"Materiality Band: {run_record.comparison.materiality_band.value}")
    if run_record.recommendation:
        typer.echo(f"Recommendation: {run_record.recommendation.recommendation.value}")
        typer.echo(f"Rationale: {run_record.recommendation.rationale}")

@app.command()
def list_simulation_strategies():
    """List available simulation strategies."""
    typer.echo("Available Strategies:")
    typer.echo("- ConservativeSandboxStrategy")
    typer.echo("- BalancedComparativeStrategy")
    typer.echo("- AdvisoryExplorationStrategy")

app.add_typer(tournaments_app, name="tournaments", help="Phase 44 Candidate Tournaments")
app.add_typer(candidate_promotion_app, name="candidate-promotion", help="Phase 45 Candidate Promotion")
app.add_typer(auto_promotion_app, name="auto-promotion", help="Phase 47 Constrained Auto Promotion")
app.add_typer(handoff_app, name="handoff", help="Phase 48 Candidate-to-Release Handoff")
app.add_typer(deployment_app, name="deploy", help="Deployment Operations")

if __name__ == "__main__":
    app()
