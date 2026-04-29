---
title: "Operator Handbook"
doc_family: "operator"
owner_role: "operations_team"
owner_component: "general"
status: "active"
---

# Operator Handbook

As an operator, your primary goal is to ensure smooth, timely, and high-quality signal generation and dispatch.

## Daily Routine
- Monitor Telegram channels for alarms or unexpected warnings.
- Execute slot runs via the CLI (`python -m sports_signal_bot.main run-slot`).
- Review the `review queue` for candidates that require manual intervention.
- Acknowledge and resolve freeze/degrade states using [Freeze/Degrade Guide](freeze_degrade_guide.md).

## Critical Actions
- Always use `--dry-run` when testing new dispatch configurations.
- Do not bypass approvals without explicitly documented override protocols.
