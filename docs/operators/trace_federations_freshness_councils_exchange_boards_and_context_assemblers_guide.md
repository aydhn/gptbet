# Operator Guide: Context Assembly

## Scope
This guide explains how to monitor and operate the context assembly layer.

## Key Operations
1. **Trace Federations**: Watch for degraded trace routes. A single stale route downgrades the federation output.
2. **Freshness Councils**: Councils require a quorum to act. If proof freshness decays and refresh evidence is absent, expect proofs to be marked stale or review_only.
3. **Exchange Boards**: Look out for blocked exchanges. A board will block exchanges if snapshots are stale.
4. **Context Assemblers**: Assemblers generate the final views for dashboards and narratives.

## CLI Commands
- `python -m sports_signal_bot.main context-assembly preview-trace-federations`
- `python -m sports_signal_bot.main context-assembly preview-proof-freshness-councils`
- `python -m sports_signal_bot.main context-assembly preview-observatory-exchange-boards`
- `python -m sports_signal_bot.main context-assembly preview-context-assemblers`
