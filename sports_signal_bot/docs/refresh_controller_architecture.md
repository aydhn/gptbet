# Refresh Controller Architecture

The Refresh Controller is a state-aware decision engine that acts on monitoring inputs to safely perform remediation actions across the ML pipeline. It serves as the automated response layer to issues identified by the monitoring and global health system (Phase 26).

## Why Monitoring Must Lead to Controlled Action

Detecting anomalies or stale artifacts is only the first half of a reliable ML Ops platform. The platform must also know how to recover from these states safely. The Refresh Controller formalizes this by explicitly separating problem classification, action candidate generation, risk assessment, and plan execution.

This ensures that:
1. Low-risk operations (e.g., catalog refresh, fallback selection) can be automated.
2. High-risk operations (e.g., retraining, recalibration) are explicitly gated and deferred for manual review or advanced scheduled execution.
3. System states like "frozen" or "degraded" are first-class concepts, ensuring the inference pipeline does not dispatch decisions based on broken or highly stale artifact chains.

## State Machine

The controller operates on a well-defined state machine:
- `healthy`: Normal operation.
- `degraded`: Operating under acceptable fallback parameters due to minor issues.
- `refresh_pending`: A remediation plan is formed and waiting to execute.
- `refreshing`: The executor is currently applying the chosen action plan.
- `refreshed`: The plan was successfully executed and validated.
- `frozen`: The system is blocked from major execution (like dispatching bets) due to unresolvable critical issues or pending manual review.
- `blocked`: Similar to frozen but specifically for a process that cannot proceed.
- `manual_review_required`: A high-risk issue requires operator intervention.
- `failed_refresh`: The automated refresh plan failed to execute or validate.
- `safe_fallback_active`: Operating specifically on a trusted fallback artifact chain.

## Refresh Action Taxonomy

Actions are categorized into families with associated risk levels:

**Low-Risk Auto Actions (Execution Allowed)**
- `catalog_refresh`
- `rerun_artifact_resolution`
- `fallback_chain_promotion`
- `cache_invalidation`
- `snapshot_reselection`
- `reload_latest_stable_artifact`
- `switch_to_stable_slot_policy`
- `enable_safe_fallback_mode`

**Medium-Risk Conditional Actions (Execution Allowed)**
- `rebuild_features_for_inference`
- `rerun_inference_step_subset`
- `rerun_dispatch_with_safe_mode`
- `refresh_source_metadata`
- `refresh_regime_inputs`

**High-Risk / Approval-Required Actions (Execution Blocked)**
- `retrain_model`
- `recalibrate_model`
- `rebuild_stacker`
- `recompute_threshold_policy`
- `recompute_policy_artifact_family`
- `refresh_sizing_policy`

## Low-Risk vs High-Risk Boundary

The boundary is strict: If an action involves fitting a model on new data, rewriting core thresholds, or making decisions that significantly alter the distribution of signals or bankroll sizing, it is classified as High Risk.

High-risk plans immediately transition the controller to `MANUAL_REVIEW_REQUIRED` and typically trigger a `frozen` state. Low-risk plans (like pointing the system back to the last known good catalog) are executed automatically if allowed by configuration.

## Freeze / Degrade Philosophy

- **Freeze**: Completely halts high-risk outbound operations (e.g., dispatching signals to Telegram/decision channels). Used when the artifact chain is broken or a high-risk refresh is required.
- **Degrade**: Allows operations to continue but at a reduced capacity or safety level (e.g., using simpler ensemble weights instead of a full stacker, or operating under stricter thresholds).

## Post-Refresh Validation

After every automated execution, the `PostRefreshValidator` verifies the outcome. It checks that the actions actually improved the freshness state and that the resulting artifact chain is valid for inference. If validation fails, the controller transitions to `failed_refresh` and usually enters a `frozen` state.

## Future Extension Paths

This phase lays the foundation for:
1. **Operator Approval Gates**: Allowing users (e.g., via Telegram inline buttons) to approve high-risk actions stuck in `manual_review_required`.
2. **Scheduled Remediation**: Moving heavy tasks like nightly retraining into a scheduled workflow rather than on-the-fly reactions.
3. **Canary Refresh & Staged Activation**: Testing a newly trained artifact chain on a shadow set before promoting it to production.
