# Telegram Dispatch Architecture

## Why Dispatch After Inference

The Telegram Dispatch layer acts as the primary operator-facing interface, ensuring that the raw outputs from the inference pipeline are converted into actionable, low-noise, and explainable messages. Instead of creating a noisy stream of automated bets, this architecture focuses on providing human operators with situational awareness through separate channels, review queues, and detailed summaries.

## Channel Taxonomy

The system segregates messages into logical channels:
*   **Decisions Channel:** High-confidence approved or candidate decisions.
*   **Review Channel:** Items requiring human verification due to uncertainty, high edge but low data quality, or model disagreement.
*   **Summaries Channel:** Slot/daily digests providing a high-level overview of system performance and activity.
*   **Warnings Channel:** Non-critical pipeline issues, stale artifacts, or minor degradations.
*   **Alarms Channel:** Critical failures such as pipeline crashes, empty universes, or unrecoverable dispatch errors.
*   **Debug Channel:** (Optional) Developer-oriented messages, dry-run outputs, and detailed trace logs.

## Routing and Severity

Messages are assigned one of several severity levels (`silent`, `info`, `warning`, `error`, `critical`). The Routing Engine uses a combination of message type, severity, inference mode, and specific context (sport/market) to determine the appropriate destination channel.

## Review Queue Philosophy

Not all signals should be acted upon automatically. The Review Queue isolates complex edge cases, such as:
*   High edge with high disagreement among models
*   High signal scores accompanied by low data quality indicators
*   Use of fallback models or stale calibrators
*   Regime risks

This ensures that operators can scrutinize high-stakes or anomalous decisions before they proceed to execution.

## Noise Control and Deduplication

To maximize the signal-to-noise ratio, the dispatch layer includes several noise-control mechanisms:
*   Duplicate suppression windows (preventing repeated alerts for the same event/market)
*   Cooldown policies
*   Low-priority message bundling
*   Summary-only modes for quiet hours or conservative operations

## Retry / Failure Handling

Network instability or API limits should not crash the inference pipeline. The delivery engine includes:
*   Configurable retry logic for transient failures
*   Classification of permanent failures
*   Fallback routing (e.g., escalating persistent failures to the alarms channel)
*   Comprehensive delivery status tracking

## Future Extension Path

The current implementation lays the groundwork for more advanced, interactive workflows in subsequent phases:
*   Operator acknowledgment (ACK)
*   Manual review actions (Approve/Reject buttons)
*   Inline system controls (e.g., freeze operations)
*   Complex escalation workflows based on time-to-acknowledge
