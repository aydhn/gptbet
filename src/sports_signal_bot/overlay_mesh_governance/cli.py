import typer
from typing import Optional
from datetime import datetime, timezone

from sports_signal_bot.overlay_mesh_governance.reporting import (
    generate_overlay_mesh_governance_summary,
    export_overlay_mesh_governance_summary,
    export_overlay_exchange_meshes,
    export_overlay_mesh_propagations,
    export_multi_tier_route_governance_records,
    export_benchmark_signal_consortiums,
    export_sovereign_resilience_baseline_registries
)
from sports_signal_bot.overlay_mesh_governance.manifests import (
    generate_overlay_mesh_governance_manifest,
    write_overlay_mesh_governance_manifest
)
from sports_signal_bot.overlay_mesh_governance.strategies import (
    ConservativeOverlayMeshStrategy,
    BalancedTieredGovernanceStrategy,
    ConsortiumFirstBaselineStrategy,
    TierStrictGovernanceStrategy,
    SovereigntyDominantBaselineStrategy
)

app = typer.Typer(help="Overlay Mesh Governance Commands")

@app.command()
def run_overlay_mesh_governance_pass():
    """Run the overlay mesh governance pipeline."""
    typer.echo("Running overlay mesh governance pass...")

    # Simulate execution
    summary = generate_overlay_mesh_governance_summary()

    export_overlay_mesh_governance_summary("results/overlay_mesh_governance_summary.json", summary)

    manifest = generate_overlay_mesh_governance_manifest()
    write_overlay_mesh_governance_manifest("results/overlay_mesh_governance_manifest.json", manifest)

    # Export empty mocks for now
    export_overlay_exchange_meshes("results/overlay_exchange_meshes.json", [])
    export_overlay_mesh_propagations("results/overlay_mesh_propagations.json", [])
    export_multi_tier_route_governance_records("results/multi_tier_route_governance_records.json", [])
    export_benchmark_signal_consortiums("results/benchmark_signal_consortiums.json", [])
    export_sovereign_resilience_baseline_registries("results/sovereign_resilience_baseline_registries.json", [])

    typer.echo(f"Governance pass complete. Health: {summary['overall_health']}")

@app.command()
def preview_overlay_meshes():
    """Preview available overlay exchange meshes."""
    typer.echo("Overlay Meshes:")
    typer.echo("- review_only_overlay_mesh (Healthy)")
    typer.echo("- bounded_projection_overlay_mesh (Healthy)")

@app.command()
def preview_route_tier_decisions():
    """Preview route tier decisions."""
    typer.echo("Route Tier Decisions:")
    typer.echo("- route_1: allow_bounded_route")
    typer.echo("- route_2: block_route_due_to_scope")

@app.command()
def preview_signal_consortiums():
    """Preview benchmark signal consortiums."""
    typer.echo("Signal Consortiums:")
    typer.echo("- treaty_benchmark_consortium (Healthy)")

@app.command()
def preview_baseline_registries():
    """Preview sovereign resilience baseline registries."""
    typer.echo("Baseline Registries:")
    typer.echo("- sovereign_resilience_baseline_registry (Healthy)")

@app.command()
def preview_overlay_mesh_governance_health():
    """Preview the overall health of the overlay mesh governance system."""
    summary = generate_overlay_mesh_governance_summary()
    typer.echo(f"Overall Governance Health: {summary['overall_health']}")

@app.command()
def list_overlay_mesh_governance_strategies():
    """List available overlay mesh governance strategies."""
    typer.echo("Available Strategies:")
    typer.echo("- ConservativeOverlayMeshStrategy (default)")
    typer.echo("- BalancedTieredGovernanceStrategy")
    typer.echo("- ConsortiumFirstBaselineStrategy")
    typer.echo("- TierStrictGovernanceStrategy")
    typer.echo("- SovereigntyDominantBaselineStrategy")

if __name__ == "__main__":
    app()
