# Approval-Gated Recovery Preparation Guide

This guide outlines the operational procedures for evaluating and approving recovery playbooks synthesized by the Remediation Copilot.

## 1. Copilot Sessions and Review Packets
When a resilience issue is detected, the Remediation Copilot generates a recommendation and bundles it into a **Review Packet**. Operators must inspect:
- **Scope**: What specific components or routes are affected?
- **Guards**: What conditions must be met for this recovery to proceed safely?
- **Rollback Notes**: How do we revert changes if the recovery path fails?

## 2. Approval Requests
The Copilot then submits an **Approval Request**. Approvals are not merely binary; they carry specific constraints:
- `max_duration_seconds`
- `allowed_step_families`
- `forbidden_conditions`

As an operator, you must ensure that these restrictions align with current platform health and policies.

## 3. Advancing to Rehearsal
Once approved, the playbook does NOT execute live. It proceeds to the **Rehearsal Phase**. Operators can monitor the Rehearsal Ledger to ensure simulations and shadow runs complete successfully without triggering stop conditions.
