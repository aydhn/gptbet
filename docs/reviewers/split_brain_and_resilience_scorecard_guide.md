# Split-Brain and Resilience Scorecard Guide

## Split-Brain Detection
When mirror members disagree on state, a split-brain is suspected. Review the `details` field of the swarm agreement to see which nodes observed what. Do not assume any single node is inherently authoritative.

## Scorecard Evaluation
Resilience Scorecards aggregate the results of game-day simulations into key dimensions like `sync_recovery_time` and `route_degradation_containment`. An overall band of `strong` indicates the system is correctly surviving and repairing simulated adverse conditions.
