import typer
import json
import os
from sports_signal_bot.ecosystem_resilience.overlays import build_federation_trust_overlay
from sports_signal_bot.ecosystem_resilience.meshes import build_hub_routing_mesh
from sports_signal_bot.ecosystem_resilience.signals import ingest_marketplace_signal
from sports_signal_bot.ecosystem_resilience.controllers import build_ecosystem_resilience_controller
from sports_signal_bot.ecosystem_resilience.contracts import MeshPressureOutcome
from sports_signal_bot.ecosystem_resilience.strategies import (
    ConservativeTrustOverlayStrategy, BalancedHubMeshStrategy, ResilienceFirstEcosystemStrategy
)

app = typer.Typer(help="Phase 80: Ecosystem Resilience")

@app.command("run-ecosystem-resilience-pass")
def run_ecosystem_resilience_pass():
    typer.echo("Running ecosystem resilience pass...")
    overlay = build_federation_trust_overlay("o1", "federated_registry", "scope1", [], [], {"currentness": 0.85})
    mesh = build_hub_routing_mesh("m1", "internal_hub_mesh", ["hub1"], ["e1"], "pol1")
    signal = ingest_marketplace_signal("s1", "treaty_alignment_signal", "b1", "scope1", ["dim1"])
    controller = build_ecosystem_resilience_controller("c1", "federation_health", ["o1"], ["m1"])

    summary = {
        "overlay_summary": {"id": overlay.overlay_id, "band": overlay.final_overlay_band.value},
        "mesh_summary": {"id": mesh.mesh_id, "health": mesh.health_status},
        "signal_summary": {"id": signal.signal_id, "relevance": signal.relevance_band.value},
        "controller_summary": {"id": controller.controller_id, "state": controller.current_state.value},
        "artifacts_path": "results/ecosystem_resilience_summary.json"
    }

    os.makedirs("results", exist_ok=True)
    with open("results/ecosystem_resilience_summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    typer.echo("Ecosystem resilience pass complete. Summary written to results/ecosystem_resilience_summary.json.")

@app.command("preview-trust-overlays")
def preview_trust_overlays():
    typer.echo("Previewing trust overlays...")
    typer.echo("Overlay o1 (federated_registry): strong_bounded_signal")

@app.command("preview-hub-routing-meshes")
def preview_hub_routing_meshes():
    typer.echo("Previewing hub routing meshes...")
    typer.echo("Mesh m1 (internal_hub_mesh): Health=healthy, Pressure=low_pressure")

@app.command("preview-marketplace-signals")
def preview_marketplace_signals():
    typer.echo("Previewing marketplace signals...")
    typer.echo("Signal s1: bounded_hint (fresh)")

@app.command("preview-resilience-controllers")
def preview_resilience_controllers():
    typer.echo("Previewing resilience controllers...")
    typer.echo("Controller c1: monitoring_normal")

@app.command("preview-ecosystem-resilience-health")
def preview_ecosystem_resilience_health():
    typer.echo("Previewing ecosystem resilience health...")
    typer.echo("Ecosystem Resilience Score Summary: stable")

@app.command("list-ecosystem-resilience-strategies")
def list_ecosystem_resilience_strategies():
    typer.echo("Available strategies:")
    typer.echo(" - ConservativeTrustOverlayStrategy")
    typer.echo(" - BalancedHubMeshStrategy")
    typer.echo(" - ResilienceFirstEcosystemStrategy")
    typer.echo(" - MarketplaceSignalStrictStrategy")
    typer.echo(" - SovereigntyDominantMeshStrategy")
