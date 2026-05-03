---
owner: "resilience-orchestrator-team"
doc_family: "reviewer-guide"
freshness_window_days: 60
---

# Recovery Guards and Confidence Guide

## Confidence Model
The Advisor computes a confidence score (Low, Guarded, Moderate, High, High with Caveats) based on pattern similarity and evidence completeness. High confidence is blocked if critical blockers exist.

## Recovery Guards
Guards intercept recovery plans before execution. Types include:
- `scope_guard`: Ensures bounding.
- `approval_guard`: Mandates human review for critical playbooks.
- `replay_guard`: Enforces replay-safe execution.

`python -m sports_signal_bot.main resilience-advisor preview-advisory-confidence`
