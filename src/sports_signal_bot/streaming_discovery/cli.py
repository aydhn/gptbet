import typer
import json
from pathlib import Path
from datetime import datetime
from typing import List

from .contracts import DiscoveryEventRecord, StreamingFabricManifest
from .topics import StreamTopic
from .events import EventFamily
from .bus import DiscoveryEventBus
from .anomaly_clusters import AnomalyClusterer
from .adaptation import AdaptiveTrustRouter
from .degradation import DegradationMonitor
from .resilience import ResilienceOrchestrator
from .observability import ObservabilityFabric
from .strategies.balanced_observability import BalancedObservabilityFabricStrategy

app = typer.Typer(help="Streaming Discovery & Observability Fabric (Phase 67)")

def setup_artifacts_dir():
    artifacts_dir = Path("artifacts/streaming_discovery")
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    return artifacts_dir

@app.command("run-streaming-discovery-pass")
def run_streaming_discovery_pass():
    """Runs a simulated stream discovery pass generating events, clusters, and adaptations."""
    typer.echo("Starting Streaming Discovery & Observability Fabric Pass...")

    # 1. Initialization
    bus = DiscoveryEventBus()
    clusterer = AnomalyClusterer()

    strategy = BalancedObservabilityFabricStrategy()
    router = AdaptiveTrustRouter(profile=strategy.get_profile())
    router.set_baseline("source_alpha", 1.0)
    router.set_baseline("source_beta", 1.0)

    degradation_monitor = DegradationMonitor()
    resilience = ResilienceOrchestrator()
    observability = ObservabilityFabric()

    # Register consumers
    bus.subscribe(StreamTopic.SYNC_EVENTS.value, "anomaly_clusterer", clusterer.process_event)
    bus.subscribe(StreamTopic.TRUST_EVENTS.value, "trust_adapter", router.process_event)
    bus.subscribe(StreamTopic.SYNC_EVENTS.value, "trust_adapter", router.process_event)

    # 2. Simulate Events (Stream)
    events = [
        DiscoveryEventRecord(event_family=EventFamily.SYNC_SUCCEEDED.value, topic_ref=StreamTopic.SYNC_EVENTS.value, source_ref="source_alpha"),
        DiscoveryEventRecord(event_family=EventFamily.SYNC_FAILED.value, topic_ref=StreamTopic.SYNC_EVENTS.value, source_ref="source_beta"),
        DiscoveryEventRecord(event_family=EventFamily.SYNC_FAILED.value, topic_ref=StreamTopic.SYNC_EVENTS.value, source_ref="source_beta"),
        DiscoveryEventRecord(event_family=EventFamily.TRUST_DOWNGRADED.value, topic_ref=StreamTopic.TRUST_EVENTS.value, source_ref="source_beta"),
        DiscoveryEventRecord(event_family=EventFamily.SYNC_FAILED.value, topic_ref=StreamTopic.SYNC_EVENTS.value, source_ref="source_beta"),
    ]

    for ev in events:
        bus.publish(ev)

    # 3. Process Stream
    typer.echo("Dispatching events to stream consumers...")
    bus.dispatch_pending()

    # 4. Evaluate Health & Resilience
    clusters = clusterer.get_clusters()
    degradation_monitor.evaluate_health(clusters)
    active_modes = degradation_monitor.get_active_modes()
    resilience.react_to_degradation(active_modes)

    snapshot = observability.capture_snapshot(
        active_subs=2,
        healthy_src=1,
        degraded_src=1,
        clusters=clusters,
        modes=active_modes
    )

    # 5. Write Artifacts
    artifacts_dir = setup_artifacts_dir()

    # Write Events
    with open(artifacts_dir / "discovery_events.json", "w") as f:
        json.dump([e.model_dump(mode='json') for e in events], f, indent=2)

    # Write Clusters
    with open(artifacts_dir / "sync_anomaly_clusters.json", "w") as f:
        json.dump([c.model_dump(mode='json') for c in clusters], f, indent=2)

    # Write Adaptations
    with open(artifacts_dir / "adaptive_routing_profiles.json", "w") as f:
        json.dump([a.model_dump(mode='json') for a in router.get_history()], f, indent=2)

    # Write Snapshot
    with open(artifacts_dir / "ecosystem_health_snapshots.json", "w") as f:
        json.dump([snapshot.model_dump(mode='json')], f, indent=2)

    # Write Manifest
    manifest = StreamingFabricManifest(
        processed_events_count=len(events),
        active_clusters=len(clusters),
        adaptations_applied=len(router.get_history()),
        health_status=snapshot.health_status,
        active_degradation_modes=[m.mode_family for m in active_modes],
        resilience_actions_taken=len(resilience.get_actions())
    )
    with open(artifacts_dir / "streaming_discovery_manifest.json", "w") as f:
        json.dump(manifest.model_dump(mode='json'), f, indent=2)

    typer.echo(f"Streaming Discovery pass complete. Manifest: {manifest.manifest_id}")
    typer.echo(f"Health Status: {manifest.health_status}")
    typer.echo(f"Active Degradation Modes: {manifest.active_degradation_modes}")
    typer.echo(f"Artifacts written to {artifacts_dir}")

@app.command("preview-discovery-events")
def preview_events():
    artifacts_dir = Path("artifacts/streaming_discovery")
    file_path = artifacts_dir / "discovery_events.json"
    if file_path.exists():
        data = json.loads(file_path.read_text())
        typer.echo(f"Found {len(data)} discovery events.")
        for d in data:
            typer.echo(f"- [{d['event_time']}] {d['event_family']} | Source: {d['source_ref']}")
    else:
        typer.echo("No discovery events found. Run 'run-streaming-discovery-pass' first.")

@app.command("preview-ecosystem-health")
def preview_health():
    artifacts_dir = Path("artifacts/streaming_discovery")
    file_path = artifacts_dir / "ecosystem_health_snapshots.json"
    if file_path.exists():
        data = json.loads(file_path.read_text())
        latest = data[-1]
        typer.echo("=== Ecosystem Health Snapshot ===")
        typer.echo(json.dumps(latest, indent=2))
    else:
        typer.echo("No health snapshots found.")

@app.command("list-streaming-discovery-strategies")
def list_strategies():
    typer.echo("Available Streaming Discovery & Adaptive Routing Strategies:")
    typer.echo("1. ConservativeStreamingRoutingStrategy")
    typer.echo("   - Adaptation bounded and slow, heavy stale penalties, strict no_safe_route.")
    typer.echo("2. BalancedObservabilityFabricStrategy (Default)")
    typer.echo("   - Balanced stream adaptation, resilient actions are practical but safe.")
    typer.echo("3. AnomalyAwareAdaptiveRoutingStrategy")
    typer.echo("   - Rapid drop of unstable sources based on cluster severity.")
    typer.echo("4. ReplayStrictStreamingStrategy")
    typer.echo("   - Prioritizes replay-required routes, degrades instantly on mismatch trends.")
    typer.echo("5. SyncStabilityFirstStrategy")
    typer.echo("   - Optimizes against route flips, very conservative adaptation.")

if __name__ == "__main__":
    app()
