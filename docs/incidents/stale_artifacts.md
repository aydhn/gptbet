---
title: "Stale Artifacts Incident"
doc_family: "incident_playbook"
owner_role: "operations_team"
owner_component: "monitoring"
status: "active"
---

# Stale Artifacts Incident

## Symptom summary
Inference or dispatch fails because the underlying model or data artifacts have not been refreshed within their required freshness window.

## Severity guidance
- HIGH: If affecting stable dispatch channel.
- MEDIUM: If affecting canary or offline evaluation.

## First 5 minutes
1. Check Telegram alarms for the exact stale artifact ID.
2. Run `python -m sports_signal_bot.main check-freshness` to identify all stale dependencies.

## Triage questions
- Is the refresh controller job failing?
- Is there a schema incompatibility preventing artifacts from saving?

## Evidence to collect
- Error logs from the latest `refresh` run.
- Current system time vs artifact generation time.

## Likely causes
- Upstream data provider outage.
- Scheduler job silently failed.

## Safe immediate actions
- Attempt manual refresh: `python -m sports_signal_bot.main run-refresh --force`

## Unsafe actions to avoid
- Do not manually override artifact timestamps to bypass checks.

## Escalation thresholds
- Escalate to `data_eng` if manual refresh fails after 2 attempts.

## Recovery path
1. Fix upstream issue or schema.
2. Force refresh artifacts.
3. Validate inference runs successfully.

## Validation after recovery
- Monitoring health score returns to > 95.

## Related commands, logs, docs
- `docs/runbooks/recovery/stale_artifact_recovery.md`
