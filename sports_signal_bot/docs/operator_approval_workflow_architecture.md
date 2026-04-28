# Operator Approval Workflow & Governance Architecture

## Why human-in-the-loop after refresh/monitoring
As the sports forecasting system matures (Phases 25-27), it becomes capable of generating complex state changes, executing logic based on predictions, triggering refreshes, and entering degraded modes. However, the system shouldn't make potentially high-risk, unrecoverable, or wide-impacting decisions without operator oversight.

This phase introduces a formal human-in-the-loop mechanism, providing a safety net where operators can systematically review and approve critical actions, while maintaining a complete, auditable ledger of those interventions.

## Request/Decision/Audit Lifecycle
1. **Creation**: The system or an operator generates an `ApprovalRequestRecord`.
2. **Queueing**: The request enters the Review Queue as a `ReviewItemRecord` categorized by urgency.
3. **Review**: The operator reviews the request through the CLI or Telegram notification.
4. **Decision**: The operator makes a decision (approve, reject, defer) producing an `ApprovalDecisionRecord`.
5. **Execution Authorization**: If approved, execution layers are authorized to proceed.
6. **Audit**: Every state change, including creation, review, and decision, is recorded in the `ApprovalLedgerRecord`.

## Review Queue Taxonomy
The Review Queue classifies requests based on risk and context:
- `decision_review_item`: Approvals on specific algorithm decisions (e.g., dispatching a specific bet).
- `refresh_review_item`: Approvals to start intensive data refreshes.
- `freeze_release_item`: Critical requests to exit a system-wide freeze state.
- `dispatch_review_item`: Approvals overriding suppressed/blocked dispatch rules.
- `anomaly_review_item`: Reviews required for identified data anomalies.
- `manual_override_item`: Requesting manual system behavior overrides.

## Override Precedence
Overrides follow a strict precedence chain to resolve conflicts:
1. Safety / freeze overrides (`force_freeze`, `force_degrade`) [Precedence: 100-90]
2. Manual block overrides (`block_market_temporarily`) [Precedence: 80]
3. Forced modes (`force_stable_only_mode`) [Precedence: 70]
4. Explicit dispatch instructions (`force_review_only_dispatch`, `allow_slot_run_once`) [Precedence: 60-40]
5. Suppressions (`suppress_noncritical_alerts`) [Precedence: 30]

## Freeze Release Governance
System freezes indicate critical instability. Releasing a freeze is subject to stricter governance:
- A specific `request-freeze-release` request must be made.
- Prerequisites must be validated (e.g., no active critical anomalies, post-refresh checks pass).
- Only operators with `senior_operator` or `admin` roles may approve.

## Role and Permission Model
- `operator`: Standard operations, alert acknowledgements, low-risk defers.
- `senior_operator`: Can approve freeze releases, high-risk refresh plans, and operational blocks.
- `reviewer`: Can only add review notes or defer items; cannot approve.
- `admin`: Has all permissions, including revoking active overrides.

## Future Extension Path
This architecture leaves clean APIs for expanding governance in future phases:
- **Multi-operator approvals**: Requiring N of M operators to sign off.
- **Scheduled approvals**: Queuing approvals for specific time windows.
- **Richer operator UIs**: Integrating the ledger into web dashboards.
- **Escalation chains**: Automatically escalating delayed requests to senior roles.
