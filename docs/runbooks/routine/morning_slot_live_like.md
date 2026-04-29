---
title: "Morning Slot Live-Like Run"
doc_family: "runbook"
owner_role: "operations_team"
owner_component: "scheduler"
status: "active"
---

# Morning Slot Live-Like Run

## Purpose
Ensure the morning snapshot contains all required data for midday inference.

## When to use
Daily at 08:00 AM UTC.

## Preconditions
- Data providers are responsive.
- Cache is healthy.

## Inputs needed
- Slot ID: `morning_live`

## Step-by-step actions
1. Run data ingestion check: `python -m sports_signal_bot.main run-refresh`
2. Run monitoring: `python -m sports_signal_bot.main run-monitoring`
3. Verify output logs for 0 errors.

## Success criteria
- Monitoring health score > 95.
- 0 critical alarms in Telegram.

## Failure branches
- If ingestion fails: refer to `docs/incidents/stale_snapshot_data.md`.
- If health score drops: refer to `docs/incidents/monitoring_health_drop.md`.

## Escalation path
Escalate to `data_eng` if provider APIs are unreachable for > 15 minutes.

## Related commands
- `python -m sports_signal_bot.main run-refresh`

## Related docs
- `docs/incidents/stale_snapshot_data.md`

## Common mistakes
- Skipping the monitoring step.

## Rollback or safe exit
N/A
