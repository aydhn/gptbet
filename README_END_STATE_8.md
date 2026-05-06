# Post-100 Hardening Pack 08: Regional Failover, Cutovers, Archive Migration, and Live-Fire Visibility

## Overview
This hardening pack introduces the resilience logic necessary for regional operations, strictly enforcing that failovers, multi-wave cutovers, archive migrations, and live-fire visibility exercises maintain bounded, caveat-preserving, and "no-safe" continuous states. It introduces the `regional-hardening` command in the `sports_signal_bot` CLI.

## Key Features
- **Regional Failover Drills**: Enforces source freshness and target readiness visibility without masking region handoff lags.
- **Multi-Wave Cutovers**: Records and preserves wave residues, rollback paths, and handoff caveats over multiple steps.
- **Archive Migration Validation**: Asserts hash continuity, lineage preservation, and replayability across relocated contexts.
- **Live-Fire Visibility**: Enforces visibility of degraded lanes, no-safe markers, and sovereignty notes under operational stress.

## Commands
```bash
python -m sports_signal_bot.main regional-hardening run-hardening-pack-08
python -m sports_signal_bot.main regional-hardening preview-regional-failover-report
python -m sports_signal_bot.main regional-hardening preview-cutover-rehearsal-report
python -m sports_signal_bot.main regional-hardening preview-archive-migration-report
python -m sports_signal_bot.main regional-hardening preview-live-fire-visibility-report
python -m sports_signal_bot.main regional-hardening preview-regional-hardening-health
python -m sports_signal_bot.main regional-hardening list-regional-hardening-strategies
```

## Why it matters
Failover honesty prevents stale secondary regions from being treated as safe. Live-fire visibility ensures that operators and reviewers do not lose track of critical sovereignty or safety boundaries when dealing with production loads.
