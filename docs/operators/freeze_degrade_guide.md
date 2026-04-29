---
title: "Freeze and Degrade Guide"
doc_family: "operator"
owner_role: "operations_team"
owner_component: "general"
status: "active"
---

# Freeze and Degrade Guide

## What is a Freeze?
A freeze stops all automated dispatches. It requires manual approval to resume. Triggered by severe anomalies (e.g., empty universe).

## What is a Degrade?
A degrade mode disables certain non-critical features (like canary evaluation) and relies entirely on stable pointers.

## Actions
- If frozen, check `monitoring` logs. Use `python -m sports_signal_bot.main release-freeze` only after verifying root cause.
