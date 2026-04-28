# Release & Promotion Architecture

The Release Management module governs the movement of artifacts (models, calibrators, thresholds, policies) from testing environments into live production (stable) usage. It enforces strict quality gates, supports incremental canary rollouts, and ensures immediate rollback capabilities.

## Release Channels

The system utilizes logical release channels to separate the stages of an artifact's lifecycle:
- **Draft**: Work in progress, not ready for evaluation.
- **Candidate**: Artifacts that have passed basic evaluation and are proposed for release.
- **Canary**: Artifacts currently undergoing limited production testing (e.g., in a subset of slots or markets) alongside the stable channel.
- **Stable**: The default, fully trusted channel for live inference.
- **Frozen**: A temporary state indicating a channel should not be updated (usually during investigations or critical anomalies).
- **Quarantined**: Artifacts identified as explicitly broken or dangerous, blocked from selection.
- **Rolled Back**: Previously stable artifacts that were reverted due to issues.
- **Archived**: Older artifacts kept for historical reference.

## Promotion Flow

1. **Request**: A `PromotionRequestRecord` is submitted to move an artifact chain (e.g., candidate -> canary).
2. **Evaluation**: The `PromotionDecisionEngine` validates the request against strict `PromotionGuards` (e.g., ensuring no quarantines, checking freeze states).
3. **Execution**: If approved, the `PromotionExecutor` updates the channel pointers in the `ChannelStateManager`.
4. **Ledger**: The action is securely logged in the append-only `ReleaseLedger`.

## Canary Validation

Before an artifact chain reaches the stable channel, it should typically run in the **Canary** channel. The `CanaryValidator` compares inference metrics (e.g., edge, log-loss) and system health snapshots between the canary and stable chains to ensure no significant performance degradation occurs.

## Rollback Philosophy

Rollbacks are treated as first-class operations. The system maintains a pointer to the `previous_stable` chain. If anomalies are detected post-promotion, a `RollbackPlanner` orchestrates an immediate and safe reversion of the stable pointer to the previous known good state, logging the event comprehensively.

## Channel-Aware Resolver

The `ArtifactResolver` dynamically selects inference artifacts based on the active channel state. It respects frozen boundaries, avoids quarantined components, and can route queries to the active canary chain when applicable.
