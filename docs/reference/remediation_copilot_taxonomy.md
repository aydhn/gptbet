# Remediation Copilot Taxonomy

## Strategies
- `ConservativeApprovalGatedCopilotStrategy`: Default. Review-heavy, rehearsal mandatory more often.
- `BalancedRecoveryPreparationStrategy`: Balanced portable playbook reuse + local safety.
- `FederationAwarePlaybookStrategy`: Heavy focus on federated playbook adaptation.
- `RehearsalFirstStrategy`: Rehearsal evidence is the heaviest factor.
- `GuardStrictSelfHealingPrepStrategy`: Conservative bounding of future automation envelopes.

## Stages
- `recommendation_generated`
- `review_packet_prepared`
- `awaiting_review`
- `awaiting_approval`
- `approved_for_rehearsal`
- `rehearsal_running`
- `rehearsal_completed`
- `readiness_evaluated`
- `ready_for_staged_execution_preparation`
- `blocked_for_execution_preparation`
- `superseded`
- `archived`
