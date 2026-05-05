# Operators Guide: Alignment Compilers

## Overview
This guide provides operational details for managing the Sovereign Governance Alignment Compilers infrastructure.

## Key CLI Commands
- `python -m sports_signal_bot.main alignment-compilers run-alignment-compilers-pass`: Runs the full compilation pipeline.
- `python -m sports_signal_bot.main alignment-compilers preview-coherence-federations`: Views the health and agreement of federated coherence scorers.
- `python -m sports_signal_bot.main alignment-compilers preview-context-dispute-tribunals`: Previews open disputes, case status, and applied caps.
- `python -m sports_signal_bot.main alignment-compilers preview-broker-exchanges`: Inspects exchange routes, constraints, and fairness metrics.
- `python -m sports_signal_bot.main alignment-compilers preview-alignment-compilers`: Views the final compiled alignment bands and applied penalties.

## Monitoring Strategies
Operators should monitor:
- **Federation Currentness**: High rates of stale federations indicate upstream issues.
- **Tribunal Backlogs**: Accumulating unresolved cases may signal missing evidence pipelines.
- **Exchange Fairness**: Ensure that strict evidence requirements aren't creating unresolvable review-only spillovers.
- **Alignment Bands**: A sudden shift to `review_only_alignment` across the board usually points to a systemic failure in `no_safe_visibility` or widespread staleness.
