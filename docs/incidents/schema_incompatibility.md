---
title: "Schema Incompatibility Incident"
doc_family: "incident_playbook"
owner_role: "data_eng"
owner_component: "schema_governance"
status: "active"
---

# Schema Incompatibility Incident

## Symptom summary
Validation errors during ingestion or inference indicating a schema mismatch.

## Severity guidance
- HIGH: Halts all subsequent data processing.

## First 5 minutes
1. Identify failing component and schema version from logs.
2. Check recent commits for schema changes.

## Triage questions
- Was a new field added as required without updating providers?
- Did a provider change their API response?

## Evidence to collect
- Pydantic validation error traces.

## Likely causes
- Provider API change.
- Uncoordinated internal schema update.

## Safe immediate actions
- Revert schema to last known good version locally if blocking critical path.

## Unsafe actions to avoid
- Do not blanket-ignore validation errors.

## Escalation thresholds
- Escalate to `core_ml` if model features are impacted.

## Recovery path
- Update schema or parsing logic to handle new structure.
- Deploy fix.

## Validation after recovery
- Zero Pydantic validation errors on refresh.

## Related commands, logs, docs
- `docs/architecture/system_overview.md`
