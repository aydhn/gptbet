# Maintenance Runbook: Streaming Discovery

## Why Scheduled Sync is Not Enough
Live ecosystems require near-real-time detection of trust drift, schema degradation, and capability staleness. The Streaming Discovery layer allows us to fail fast and route around anomalies before the next scheduled batch sync.

## Consumer Lag Spikes
If `EventCursorRecord.is_stalled` is true or `lag_events_count` spikes:
1. Verify the consumer callback logic for infinite loops or blocking I/O.
2. Check the `ObservabilityFabric` metrics to ensure the system hasn't entered a severe `overlay_rebuild_storm`.

## Future Extensions
This phase lays the groundwork for:
- Real streaming buses (Kafka, NATS, Redis Streams) via external relay adapters.
- Federated telemetry meshes.
- Automated resilient recovery loops.
