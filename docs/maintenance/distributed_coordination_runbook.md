# Distributed Coordination Runbook

## Daily Operations
Run the daily distributed coordination pass to execute token allocations, detect contentions, and process council decisions.
`python -m sports_signal_bot.main distributed-coordination run-distributed-coordination-pass`

## Inspection Commands
- Preview Clusters: `python -m sports_signal_bot.main distributed-coordination preview-coordination-clusters`
- Preview Pools: `python -m sports_signal_bot.main distributed-coordination preview-broker-pools`
- Preview Councils: `python -m sports_signal_bot.main distributed-coordination preview-council-cases`

## Troubleshooting Failovers
If a failover is stuck in a cautious or blocked state, inspect the failover records:
`python -m sports_signal_bot.main distributed-coordination preview-failover-records`
Ensure that the target node has a valid snapshot. If the snapshot lineage is broken, manual revalidation is required.
