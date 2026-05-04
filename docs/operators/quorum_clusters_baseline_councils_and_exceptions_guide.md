# Operators Guide: Quorum Clusters, Baseline Councils, and Exceptions

## Overview

This guide explains how operators interact with the governance exceptions layer via the CLI. The focus is on reviewing exchange health, managing backplane clusters, observing baseline council adjudications, and reviewing exception ledgers.

## Key CLI Commands

- `python -m sports_signal_bot.main run-governance-exceptions-pass`: Runs the complete validation pass over exchanges, clusters, councils, and exceptions.
- `python -m sports_signal_bot.main preview-quorum-exchanges`: Inspects active quorum exchanges.
- `python -m sports_signal_bot.main preview-backplane-clusters`: Checks cluster capacity and pressure.
- `python -m sports_signal_bot.main preview-baseline-councils`: Reviews currentness/applicability dispute outcomes.
- `python -m sports_signal_bot.main preview-governance-exception-ledgers`: Reviews the expiry and replay health of exceptions.

## Common Operations

1. **Investigating Downgraded Exchanges:** If an exchange shows up as `exchanged_review_only`, check the backplane cluster backpressure or missing caveats using `preview-quorum-exchanges` and `preview-backplane-clusters`.
2. **Reviewing Unresolved Councils:** A council case may remain open if evidence is stale. Review via `preview-baseline-councils`.
3. **Monitoring Exception Expiries:** Exceptions have strict validity windows. Monitor `preview-governance-exception-ledgers` to ensure exceptions aren't stuck in active states inappropriately.
