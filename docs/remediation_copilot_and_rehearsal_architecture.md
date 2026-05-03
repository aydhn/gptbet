# Remediation Copilot and Rehearsal Architecture

This document describes the Remediation Copilot layer, which bridges the gap between autonomous resilience advisory (Phase 69) and safe, approval-gated recovery execution preparation.

## Core Concepts

1. **Copilot Assists, Human/Policy Decides**: The system recommends recovery actions, but execution requires structured approvals.
2. **Review Packets**: Recommendations are packaged into review packets detailing scope, guards, rollback notes, and expected signals.
3. **Approval-Gated Flow**: Structured approvals dictate the allowable scope and duration of recovery preparation.
4. **Rehearsal Ledgers**: Playbooks must often be rehearsed in simulation or shadow mode before live execution readiness.
5. **Portable Playbook Federation**: Playbooks can be exported and imported across trust domains, subject to strict local safety adaptation.
6. **Bounded Self-Healing Preparation**: Identifies candidates for future automation, explicitly defining their automation envelopes (boundaries and guards) without enacting actual self-healing yet.

## Components

- `sessions.py`: Manages the copilot session state machine.
- `reviews.py`: Builds comprehensive review packets for human/policy evaluation.
- `approvals.py`: Handles structured approval requests and scopes.
- `rehearsals.py`: Orchestrates rehearsal simulations and maintains the rehearsal ledger.
- `readiness.py`: Computes whether a recovery plan is ready for staged execution preparation.
- `federation.py` & `adaptation.py`: Manages portable playbook exports, imports, and local safety adaptations.
- `automation_prep.py`: Evaluates and bounds self-healing candidates for future automation.

## Strategy Taxonomy

- `ConservativeApprovalGatedCopilotStrategy`
- `BalancedRecoveryPreparationStrategy`
- `FederationAwarePlaybookStrategy`
- `RehearsalFirstStrategy`
- `GuardStrictSelfHealingPrepStrategy`
