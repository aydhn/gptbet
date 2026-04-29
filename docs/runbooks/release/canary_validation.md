---
title: "Canary Validation Runbook"
doc_family: "runbook"
owner_role: "platform"
owner_component: "release"
status: "active"
---

# Canary Validation Runbook

## Purpose
Validate a candidate model running in the canary channel.

## When to use
Before promoting a canary to stable.

## Preconditions
- Canary has run for at least 48 hours without critical incidents.

## Inputs needed
- Candidate ID
- Stable Model ID

## Step-by-step actions
1. Run quality check: `python -m sports_signal_bot.main check-canary-quality --candidate <ID>`
2. Compare metrics with stable.
3. If metrics are better or equivalent, trigger promotion approval.

## Success criteria
- Quality gate passes.
- Promotion approved in the registry.

## Failure branches
- If quality fails, quarantine candidate: refer to rollback runbook.

## Escalation path
Escalate to `core_ml` if metrics show unexpected degradation.

## Related commands
- `python -m sports_signal_bot.main check-canary-quality`

## Related docs
- `docs/governance/release_governance.md`

## Common mistakes
- Promoting without reviewing side-by-side performance logs.

## Rollback or safe exit
Quarantine candidate and leave stable pointer untouched.
