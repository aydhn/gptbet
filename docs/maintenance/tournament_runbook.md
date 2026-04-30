---
title: Tournament Runbook
owner: Operations
family: runbook
freshness: P30D
---

# Tournament Operations Runbook

**Commands**:
- `python -m sports_signal_bot.main tournaments run-tournament --family threshold_tournament`
- `python -m sports_signal_bot.main tournaments preview-pareto-front --tournament-id <id>`

**Troubleshooting**:
- *Empty Fronts*: Check if constraints blocked all candidates.
- *Incomparable Candidates*: Ensure all candidates in the batch target the same parameter family.
