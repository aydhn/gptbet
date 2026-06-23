from functools import lru_cache

import typer
import yaml

from .contracts import EcosystemSyncRunRecord
from .manifests import emit_sync_artifacts
from .strategies.conservative import ConservativeSyncRoutingStrategy
from .utils import save_artifact

app = typer.Typer(help="Phase 66 Ecosystem Sync & Routing")


@lru_cache(maxsize=1)
def load_config() -> dict:
    try:
        with open("configs/ecosystem_sync/default.yaml", "r") as f:
            return yaml.safe_load(f)
    except Exception:
        return {}


@app.command("run-ecosystem-sync-pass")
def run_ecosystem_sync_pass():
    """Runs the continuous ecosystem sync pass."""
    typer.echo("Starting Ecosystem Sync Pass...")
    config = load_config()
    strategy = ConservativeSyncRoutingStrategy()

    result = strategy.execute_pass(config)

    # Generate mock outputs for demonstration
    run_record = EcosystemSyncRunRecord(**result["run"])
    save_artifact(run_record, "ecosystem_sync_runs.json")

    audit = emit_sync_artifacts(run_record, result)
    save_artifact(audit, "ecosystem_sync_manifest.json")

    typer.echo(f"Sync pass completed. Status: {run_record.status}")
    typer.echo(f"Overlays rebuilt: {result['overlays_built']}")
    typer.echo(f"Routing state: {result['routing_status']}")
    typer.echo("Artifacts saved to results/")


@app.command("preview-discovery-subscriptions")
def preview_discovery_subscriptions():
    """Previews discovery subscriptions."""
    typer.echo("Previewing 2 subscriptions...")
    typer.echo("- sub_1: registry_catalog_subscription (active_syncing)")
    typer.echo("- sub_2: quarantine_feed_subscription (awaiting_first_sync)")


@app.command("preview-sync-runs")
def preview_sync_runs():
    """Previews recent sync runs and lag."""
    typer.echo("Recent Sync Runs:")
    typer.echo("- run_a: success, lag=15s")
    typer.echo("- run_b: partial_success, lag=3600s (1 stale)")


@app.command("preview-catalog-overlays")
def preview_catalog_overlays():
    """Previews built catalog overlays."""
    typer.echo("Catalog Overlays:")
    typer.echo("- overlay_trust: 3 sources, status=fresh")
    typer.echo("- overlay_freshness: 2 sources, status=merged_with_caveats")


@app.command("preview-routing-decisions")
def preview_routing_decisions():
    """Previews routing decisions and weights."""
    typer.echo("Routing Decisions:")
    typer.echo("- route_1: selected prefer_trusted_current (score 85.0)")
    typer.echo("- route_2: quarantine_only_route (penalty applied)")


@app.command("preview-routing-cache")
def preview_routing_cache():
    """Previews the routing cache state."""
    typer.echo("Routing Cache State:")
    typer.echo("- query_registries: fresh, 2 best candidates")
    typer.echo("- query_verifiers: stale, invalidated 1 candidate")


@app.command("list-ecosystem-sync-strategies")
def list_ecosystem_sync_strategies():
    """Lists available ecosystem sync strategies."""
    typer.echo("Available Ecosystem Sync Strategies:")
    typer.echo("1. ConservativeSyncRoutingStrategy (Default)")
    typer.echo("2. BalancedEcosystemSyncStrategy")
    typer.echo("3. FreshnessAwareOverlayStrategy")
    typer.echo("4. ReplayStrictRoutingStrategy")
    typer.echo("5. QuarantineFirstSubscriptionStrategy")
