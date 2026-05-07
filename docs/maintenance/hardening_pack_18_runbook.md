# Maintenance Runbook: Hardening Pack 18

## Execution
Run `python -m sports_signal_bot.main continuity-arbitration-hardening run-hardening-pack-18` to generate updated continuity artifacts.

## Diagnostics
Use `preview-continuity-arbitration-health` to inspect the overarching health state of all arbitration rails and ledgers. Any release blockers flagged must be addressed by restoring proof freshness or explicitly authorizing the degraded lane.
