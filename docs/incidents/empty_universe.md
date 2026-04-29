---
title: "Empty Universe Incident"
doc_family: "incident_playbook"
owner_role: "operations_team"
owner_component: "inference"
status: "active"
---

# Empty Universe Incident

## Symptom summary
The signal universe returns 0 eligible candidates for a given slot.

## Severity guidance
- HIGH: If unexpected during an active sports day.
- LOW: If expected (e.g., off-season).

## First 5 minutes
1. Check Telegram alarms for universe size.
2. Verify downstream provider data is populated.

## Triage questions
- Are there matches scheduled for today?
- Did a schema change drop valid features?

## Evidence to collect
- Output of `python -m sports_signal_bot.main run-refresh`
- Upstream schedule data.

## Likely causes
- Empty upstream data.
- Overly strict filtering logic applied recently.

## Safe immediate actions
- Confirm schedule externally (e.g., sports website).

## Unsafe actions to avoid
- Do not manually insert dummy data to bypass checks.

## Escalation thresholds
- Escalate to `data_eng` if schedule shows matches but universe is empty.

## Recovery path
- Correct upstream ingestion filters.
- Re-run ingestion and inference.

## Validation after recovery
- Universe size > 0.

## Related commands, logs, docs
- `docs/runbooks/routine/morning_slot_live_like.md`
