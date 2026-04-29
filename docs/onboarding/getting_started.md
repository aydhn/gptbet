---
title: "Getting Started (30-Minute Tour)"
doc_family: "onboarding"
owner_role: "operations_team"
owner_component: "general"
status: "active"
---

# Getting Started: The 30-Minute Tour

Welcome! This guide gets you up to speed on operating the Sports Signal Bot.

## Core Concepts
- **Slot:** A predefined time window when predictions are generated and dispatched.
- **Freeze:** A safety mechanism that halts dispatch when critical anomalies occur.
- **Canary:** A shadow deployment of a new model/artifact evaluating live without dispatching.

## First Day Checklist
Read `docs/onboarding/day1_checklist.md`.

## Key Commands
Try running this safely:
`python -m sports_signal_bot.main run-slot --dry-run`

## Where to get help
Check the [Glossary](../reference/glossary.md) or the [FAQ](../reference/faq.md).
