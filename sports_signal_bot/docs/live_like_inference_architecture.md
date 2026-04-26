# Live-Like Inference Architecture

## Why Inference After Research Stack?
The research stack (Phases 1-23) builds robust, time-aware validation, model artifacts, sizing strategies, and portfolio tracking. The inference phase bridges the gap between research and operations. It turns the "sum of research modules" into an operational pipeline that can be run on a schedule, resolve the latest artifacts, and produce actionable decision packets.

## Snapshot-Based Execution
Every inference run is based on a snapshot in time. It captures the available event universe and market data at that moment. This prevents lookahead bias and ensures that the system makes decisions exactly as it would in production.

## Artifact Resolution Chain
The inference engine must resolve a compatible chain of artifacts for a given sport and market:
- Feature Config
- Base Model
- Calibrator
- Ensemble
- Stacker
- Threshold Policy
- Execution Policy
- Sizing Strategy
- Portfolio Strategy

If an artifact is missing or incompatible, the system gracefully degrades (e.g., falling back from a stacker to an ensemble, or from calibrated probabilities to raw probabilities, with appropriate warnings).

## Slots and Batch Windows
Inference runs are orchestrated via "slots" (e.g., morning, midday, evening). Each slot defines:
- The lookahead window for events
- The data freshness requirement
- The preferred artifact resolution policy (e.g., `latest_compatible` vs `latest_stable`)
- The output profile

## Decision and Review Packets
The pipeline produces two main outputs per event:
1.  **InferenceDecisionPacket**: Designed for operational consumption (Telegram dispatch, actual execution). Contains final probabilities, action class, and stake.
2.  **InferenceReviewPacket**: Designed for diagnostics and post-analysis. Contains detailed breakdowns of dynamic weights, regime tags, and threshold rationales.

## Future Extension Path
This architecture provides clean interfaces for future phases:
-   **Telegram Dispatch**: Can consume the `InferenceDecisionPacket`.
-   **Self-Refresh / Scheduled Runs**: Can orchestrate `InferenceRunner` based on cron/slots.
-   **Health Monitoring & Live Gating**: Can intercept the pipeline steps using `PipelineStepResult`.
