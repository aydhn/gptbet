---
owner: "resilience-orchestrator-team"
doc_family: "runbook"
freshness_window_days: 30
---

# Resilience Advisor Runbook

## Daily Checks
1. Run `run-resilience-advisor-pass` to ensure no errors.
2. Check `preview-advisory-confidence` for spikes in `low` confidence.

## Troubleshooting
- If `no_safe_advice` rate spikes, check if old patterns are overly penalized or if a novel incident family has emerged without simulation coverage.
- If playbook synthesis fails, check `configs/resilience_advisor/playbooks.yaml` for missing step definitions.
