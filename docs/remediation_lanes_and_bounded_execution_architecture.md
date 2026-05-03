# Phase 71: Remediation Lane Architecture & Bounded Execution

## Overview
This phase introduces semi-autonomous, explicit boundary **Remediation Lanes**. Instead of blanket execution rights, lanes are granted short-lived **Bounded Execution Tokens** derived from approvals. Execution is gated by rigorous readiness checks and concluded strictly by a **Closed-Loop Verification**.

## Bounded Execution Token Model
Tokens are NOT approvals; they are the *manifestation* of an approval bound by time, scope, and explicitly allowed step families. If a token expires or its lane scope is exceeded, execution is halted immediately.

## Review-Aware Execution
Even semi-autonomous lanes are "review-aware". Unresolved reviewer caveats project down to the lane and can downgrade a staged execution token into a `review_only_execution_token`.

## Closed-Loop Recovery Readiness
No execution is considered "complete" until closed-loop verification occurs. The system matches `LaneCheckpointRecord` and `LaneStopConditionRecord` against expected outcomes. A rollback requirement is strictly enforced.

## Federated Playbook Catalogs
Playbooks imported from federated catalogs cannot be executed natively. They are treated as external listings and pass through an adaptation layer to become review-only or safe local lanes.
