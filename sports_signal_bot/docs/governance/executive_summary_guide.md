---
owner_role: lead_engineer
doc_family: governance
freshness_window_days: 180
last_reviewed: 2026-04-28
---

# Executive Summary Generation Guide

## Purpose
The Executive Summary provides high-level stakeholders with a concise overview of system health, key performance indicators (KPIs), wins, and risks without overwhelming technical detail.

## Generating the Report
Run the following CLI command:
```bash
python -m sports_signal_bot.main reporting run-reporting --audience executive --period weekly
```

## Report Contents
- **Overall Status**: A brief narrative of system health.
- **Top KPIs**: Usually includes Slot Health Score, Bankroll Return, and Release Promotion Stability.
- **Key Wins & Risks**: Selected highlights automatically deduced from significant positive or negative metric shifts.
- **Immediate Attention Items**: Critical warnings generated during the reporting period.

## Future Extensibility
This report bundle architecture is designed to easily integrate with future BI tools or scheduled email summaries via the JSON manifest outputs.
