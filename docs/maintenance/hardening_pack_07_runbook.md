# Maintenance Runbook: Hardening Pack 07

1. Run standard pack verification:
   `python -m sports_signal_bot.main migration-hardening run-hardening-pack-07`
2. Check `artifacts/migration_hardening/migration_hardening_health_report.json` for release blockers.
3. If release blockers > 0, review the specific lane, drill, chain, or game that failed and resolve the missing check.
