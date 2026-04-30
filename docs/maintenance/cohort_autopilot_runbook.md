---
owner: Principal Adoption Autopilot Engineer
family: runbooks
freshness_window_days: 60
---

# Cohort Autopilot Maintenance Runbook

## Daily Checks
1. Run `python -m sports_signal_bot.main cohort-autopilot preview-adoption-cohorts`.
2. Check for paused cohorts and investigate causes.
3. Review fleet pressure.

## Troubleshooting
- **Autopilot Blocked:** Check if `stale_verification_block_hours` has been exceeded.
- **Unexpected Rollbacks:** Review the `rollback.yaml` thresholds.
