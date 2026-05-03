# Sports Signal Bot

Sports Signal Bot is an advanced ecosystem for sports forecasting, orchestration, discovery, and governance.

## Features

- Verifier Portal
- Ecosystem Discovery
- Evidence & Explainability
- Transparency
- Streaming Discovery & Observability Fabric (Phase 67)

## Getting Started

1. Set up the environment
2. Run `python -m sports_signal_bot.main --help`

## Streaming Discovery & Observability Fabric

The streaming discovery and observability fabric layer operates on events as signals, adapting routes based on anomalies and ensuring visibility into ecosystem health.

## Resilience Advisor & Recovery Orchestration (Phase 69)
The system includes an autonomous, bounded resilience advisor that observes failure patterns and synthesizes safe, reviewable remediation playbooks and orchestration plans. See `docs/resilience_advisor_and_recovery_orchestration_architecture.md` for details.

## Remediation Lane Architecture & Bounded Execution (Phase 71)

The remediation lane layer divides automated recovery into safe, narrow lanes. Instead of blanket automation, recovery steps must pass readiness gates and operate under short-lived Bounded Execution Tokens derived from review approvals.
- Execution is strictly bounded by scope, token validity, and step families.
- All lanes must achieve Closed-Loop Verification to be considered completed.
- Federated playbook catalogs can safely exchange recovery plans which must be adapted locally.

Run `python -m sports_signal_bot.main remediation-lanes run-remediation-lanes-pass` to simulate lane eligibility, token issuance, closed-loop readiness, closure verification, federated catalog adaptation, and automation preparation.

### Phase 73: Supervised Execution Coordination Fabric
The system now includes an Execution Coordination Fabric that provides safe, bounded concurrency for multiple remediation lanes. Rather than acting as a general-purpose scheduler, it explicitly coordinates contention over shared surfaces (like data sources, rollback paths, and token capacity) to ensure safety always takes precedence over parallelism.

Core mechanisms:
* **Approval-Token Broker**: Manages token allocation and renewals centrally to prevent exhaustion and unauthorized scope widening.
* **Contention Arbitration Engine**: Detects shared dependencies and arbitrates conflicts based on strict safety precedence (e.g., rollback or closure priority always preempts opportunistic repair).
* **Multi-Lane Scheduler**: Evaluates lane readiness and schedules runtime windows based on broker and arbitration decisions.
* **Coordination Ledger**: Maintains an audit trail of all scheduling and brokerage decisions for explainability.

**Key CLI Commands:**
- `python -m sports_signal_bot.main execution-coordination run-execution-coordination-pass`
- `python -m sports_signal_bot.main execution-coordination preview-multi-lane-schedules`
