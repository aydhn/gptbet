# Streaming Discovery & Observability Fabric Architecture (Phase 67)

## Overview
This phase elevates the ecosystem from batch/scheduled syncs to a continuous, streaming-oriented architecture. It introduces an internal Event Bus that processes discovery, synchronization, overlay, and capability negotiation events in near-real-time.

Events are treated as **signals**, not absolute sources of truth. They drive adaptive trust routing, anomaly clustering, and dynamic degradation modes while maintaining strong lineage and explicit safety bounds.

## Core Components
1. **Discovery Event Bus**: In-memory message bus routing events (topics: `sync_events`, `routing_events`, etc.) to consumers via envelopes.
2. **Anomaly Clusterer**: Groups repeated errors (e.g., sync failures, freshness decays) by root cause heuristics instead of logging isolated incidents.
3. **Adaptive Trust Router**: Dynamically adjusts routing weights based on stream signals within strict policy bounds.
4. **Degradation Monitor**: Enters explicit degraded modes (e.g., `routing_degraded_mode`) when anomaly thresholds are breached.
5. **Observability Fabric**: Generates `EcosystemHealthSnapshotRecord` to make the entire mesh visible, exposing lags, conflicts, and health statuses.

## Design Principles
- **Events are Signals, Not Authority**: Verified state transitions are still governed by strict capability negotiation and cryptographic assurance. Stream events provide *hints* for adaptation.
- **Adaptation Must Be Bounded**: Weights can only shift within `max_trust_weight_change` bounds defined in `AdaptiveRoutingProfileRecord`.
- **Degraded Modes are Explicit**: The system never silently falls back. It explicitly declares degraded mode states and executes `ResilienceActionRecord` paths.
