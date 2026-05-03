---
owner: "resilience-orchestrator-team"
doc_family: "operator-guide"
freshness_window_days: 60
---

# Pattern Memory and Playbook Synthesis Guide

## Pattern Memory
The system continuously observes incidents and indexes them into the `FailurePatternMemory`. Operators can query this via:
`python -m sports_signal_bot.main resilience-advisor preview-failure-pattern-memory`

## Synthesis
When an incident is detected, the Advisor matches the signature against memory to synthesize a playbook.
`python -m sports_signal_bot.main resilience-advisor preview-remediation-playbooks`

## Stale Patterns
Patterns decay over time and are penalized if their historical playbooks consistently fail.
