---
owner: "Platform Ops"
family: "runbook"
freshness_window: "15d"
---

# Handoff Runbook

## Daily Ops
1. Run `python -m sports_signal_bot.main preview-handoff-candidates`
2. Address held candidates.

## CLI Commands
- `run-handoff-pass`: Execute the final readiness handoff evaluation pipeline.
- `preview-readiness-matrix`: View the dimension scores.
- `preview-activation-bridge`: View the bridge package constraints.
