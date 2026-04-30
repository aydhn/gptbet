---
owner_role: "review_team"
doc_family: "runbook"
freshness_days: 30
---

# Why-Not and Dispute Guide

Use `python -m sports_signal_bot.main evidence explain-why-not --event-id <id>` to see why an event was NOT traded.

It will list the exact blocking claims (e.g. low edge, max portfolio exposure). Counterfactual hints may suggest what needed to change for approval.
