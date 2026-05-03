# Registry Conformance Runbook

1. Run the conformance pass: `python -m sports_signal_bot.main registry-conformance run-registry-conformance-pass`
2. Preview registry health: `python -m sports_signal_bot.main registry-conformance preview-registry-health`
3. If health is degraded due to stale entries, issue renewals for the affected treaties/corridors.
4. Review benchmark deviations: `python -m sports_signal_bot.main registry-conformance preview-benchmark-comparisons`
