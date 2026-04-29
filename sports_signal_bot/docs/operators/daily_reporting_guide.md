---
owner_role: operator
doc_family: runbook
freshness_window_days: 30
last_reviewed: 2026-04-28
---

# Daily Reporting Guide for Operators

## Purpose
Operators use the `operator` audience profile to view daily system execution metrics, current incidents, and operational health summaries.

## How to Generate the Report
Run the following CLI command to generate a daily report bundle:
```bash
python -m sports_signal_bot.main reporting run-reporting --audience operator --period daily
```

## Reviewing Output
- Check `artifacts/reporting/report_bundle.md` for a readable markdown summary.
- The summary will include:
  1. Ops Health Summary
  2. Daily Metrics
  3. Current Incidents
- Any warnings or caveats will be explicitly listed at the bottom of the report.

## Handling Incidents
If the `slot_health_score` is below acceptable thresholds, or `current_incidents` lists unresolved items, refer to the incident response runbooks to stabilize the system.
