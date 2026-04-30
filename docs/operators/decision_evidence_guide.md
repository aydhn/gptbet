---
owner_role: "operations_team"
doc_family: "operator"
freshness_days: 30
---

# Decision Evidence Guide

Use `python -m sports_signal_bot.main evidence explain-decision --event-id <id>` to understand why a decision was reached.

Pay attention to:
- **Confidence Band**: If it's "low" or "disputed", manual review is advised.
- **Caveats**: System warnings about stale data or partial coverage.
