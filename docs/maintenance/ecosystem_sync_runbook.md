---
owner: ecosystem_sync_team
family: runbook
freshness_window_days: 30
---

# Ecosystem Sync Runbook

## Daily Operations
Run the sync pass daily or on a schedule:
`python -m sports_signal_bot.main ecosystem-sync run-ecosystem-sync-pass`

## Incident Response
**Sync Lag Spikes:** Check network connectivity to sources and adjust `max_concurrent_syncs`.
**Quarantine Clusters:** If many subscriptions enter quarantine simultaneously, verify external directory consistency and notarization status.

## Clearing Cache
If routing becomes unsafe, force an invalidation of the routing cache via internal CLI commands.
