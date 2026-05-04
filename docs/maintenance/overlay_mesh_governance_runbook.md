# Maintenance: Overlay Mesh Governance

## Routine Maintenance
1. Run `python -m sports_signal_bot.main overlay-mesh-governance run-overlay-mesh-governance-pass` to trigger checks and produce governance artifacts.
2. Review the output summaries, especially baseline supersessions and consortium suppressions.

## Diagnostics
If routes are blocked unexpectedly, check the tiers. Ensure no `sovereignty_guard_tier` or `local_scope_tier` is correctly triggering a deny. Check the baseline registries for stale current pointers.
