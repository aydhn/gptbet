# Operators Guide: Dashboards, Boards, Clearing & Narratives

This guide explains how to manage and monitor the outputs of the Phase 91 assurance exchange.

## Command Reference
`python -m sports_signal_bot.main assurance-exchange run-assurance-exchange-pass`
Runs a complete pass of the assurance exchange components including board resolution and narrative compilation.

## Previews
- `preview-dashboard-exchanges`
- `preview-federation-boards`
- `preview-replay-clearing`
- `preview-assurance-narratives`

## Caveats and Exceptions
- Stale snapshots will inherently downgrade dashboard exchange quality.
- Replay matching without required evidence will block progress.
- Operator actions must preserve 'no safe' visibility constraints.
