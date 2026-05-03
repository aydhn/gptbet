# Portable Playbook Adaptation and Readiness Guide

This guide details the review process for imported Portable Playbooks and the subsequent Execution Readiness evaluations.

## 1. Playbook Federation and Adaptation
Federated playbooks imported from external trust domains must undergo local adaptation before they can be considered for execution. Reviewers must ensure:
- Local restrictions (e.g., `unsafe_semantic_widening`) are correctly applied.
- The adaptation outcome is explicitly logged (e.g., `adapted_clean`, `adapted_with_restrictions`, `quarantined_for_manual_mapping`).

## 2. Execution Readiness
A playbook is only ready for staged execution preparation if it meets the following criteria:
- **Approval Completeness**: All required human/policy approvals are logged.
- **Rehearsal Success**: The rehearsal ledger shows a completed, successful shadow run.
- **Guard Pass Status**: All requisite guards have passed in the simulated environment.
- **Rollback Completeness**: Rollback steps are fully defined and tested.

Reviewers must explicitly clear any blockers (e.g., `approval_incomplete`) before marking a plan as `staged_execution_preparation_ready`.
