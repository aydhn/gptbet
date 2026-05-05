---
title: Operators Guide for Consistency Ledgers (Phase 98)
family: consistency_ledgers
owner_role: Principal Alignment Federation Engineer
freshness_window: 90d
---

# Operators Guide

## CLI Commands

- `python -m sports_signal_bot.main consistency-ledgers list-consistency-ledger-strategies`
  - Lists the available strategies (e.g., `balanced`, `conservative`).
- `python -m sports_signal_bot.main consistency-ledgers run-consistency-ledgers-pass --strategy balanced`
  - Executes the full pipeline: builds federations, routes meshes, executes clearers, and updates ledgers.
- `python -m sports_signal_bot.main consistency-ledgers preview-consistency-ledgers`
  - Shows the current contradictions and state shifts in the ledger.

## Responding to Pressure

If you see `MeshPressureState.CRITICAL` in the tribunal mesh previews:
- Investigate stale nodes using `preview-tribunal-meshes`.
- The system will automatically suppress non-critical paths to protect the mesh. This is working as intended to prevent scope expansion under duress.

If you see `ClearingOutcome.CLEARED_DEGRADED_EVIDENCE_ROUTE`:
- This indicates that a critical request was matched with a listing that has very poor evidence completeness. Review the `warnings` list for the specific match ID to identify the gap.
