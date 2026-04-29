---
title: "Monitoring Health Drop"
doc_family: "incident_playbook"
owner_role: "operations_team"
owner_component: "monitoring"
status: "active"
---

# Monitoring Health Drop

## Symptom summary
System health score drops below 90, triggering warnings. Drops below 80 trigger system freeze.

## Severity guidance
- CRITICAL: Score < 80 (Freeze Active)
- MEDIUM: Score < 90

## First 5 minutes
1. Check Telegram for `HealthReport`.
2. Identify the sub-component failing (Data, Inference, Dispatch, Cache).

## Triage questions
- Did a recent schema update occur?
- Is cache returning corrupted data?

## Evidence to collect
- Run `python -m sports_signal_bot.main run-monitoring --verbose`

## Likely causes
- Outdated data snapshots.
- Sub-component timeouts.

## Safe immediate actions
- None if frozen. Wait for triage.

## Unsafe actions to avoid
- Do not use `release-freeze` until the root cause is resolved.

## Escalation thresholds
- Escalate immediately if score < 80 and cause is unknown.

## Recovery path
- Resolve underlying component failure.
- Re-run monitoring to clear freeze.

## Validation after recovery
- Health score > 95.

## Related commands, logs, docs
- `docs/operators/freeze_degrade_guide.md`
