# Operator Guide: Event Bus, Routing & Degradation

## Commands
- `python -m sports_signal_bot.main streaming-discovery run-streaming-discovery-pass`: Simulates processing the event stream, emitting clusters, updating route weights, and capturing health snapshots.
- `python -m sports_signal_bot.main streaming-discovery preview-ecosystem-health`: Views the latest snapshot.
- `python -m sports_signal_bot.main streaming-discovery list-streaming-discovery-strategies`: Lists available routing strategies.

## Handling Degradation Modes
When the ecosystem snapshot shows `health_status: degraded`, check the active `degradation_modes`.
- Identify the anomaly cluster driving the degradation via `artifacts/streaming_discovery/sync_anomaly_clusters.json`.
- The system will automatically execute resilience actions (like suppressing a stale source). Do not manually mutate the routing tables unless the cluster is identified as a false positive.
