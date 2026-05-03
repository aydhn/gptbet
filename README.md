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
