---
owner: ecosystem_sync_team
family: operator_guide
freshness_window_days: 60
---

# Subscriptions, Overlays, and Routing Guide

This guide details how to operate the Ecosystem Sync layer.

## Managing Subscriptions
Subscriptions are defined by policies in `configs/ecosystem_sync/subscriptions.yaml`. They dictate how often sources are synced and when they should be quarantined.

## Inspecting Overlays
Overlays merge multiple sources into a single view. If sources conflict, the overlay merge logic resolves it based on `configs/ecosystem_sync/overlays.yaml` rules, potentially marking entries with caveats or placing them in quarantine.

## Routing Output
Routing is an explicit recommendation engine, not an implicit acceptance. Use `python -m sports_signal_bot.main ecosystem-sync preview-routing-decisions` to review the current trust-weighted routing scores and rationales.
