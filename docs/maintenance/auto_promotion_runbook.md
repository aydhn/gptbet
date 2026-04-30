---
owner: ops
family: runbook
freshness_window_days: 90
---

# Auto Promotion Runbook

## Normal Operation
Run the pass periodically via CRON or equivalent workflow orchestrator:
```bash
python -m sports_signal_bot.main auto-promotion run-auto-promotion-pass
```

## Previewing (Dry-Run)
To safely preview how the heuristics engine evaluates the current fleet without recording quotas or advancing states:
```bash
python -m sports_signal_bot.main auto-promotion preview-auto-progression
```

## Handling Quota Pressure
If `blocked_by_capacity` decisions are high, verify if `configs/auto_promotion/default.yaml` quotas need adjusting:
- `max_auto_progressions_per_run`
- `max_auto_kills_per_run`

Only increase if system stability is high and reviewer backlog is clear.

## Manual Overrides
To block a problematic candidate from auto-promotion, apply a manual hold in the candidate state. This will result in `blocked_by_manual_override` during the next pass.
