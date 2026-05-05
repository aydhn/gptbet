# Maintenance Runbook: Alignment Compilers

## Handling Widespread Stale Federations
1. Check upstream Coherence Scorers.
2. Verify that Proof Catalogs are updating.
3. Use `preview-coherence-federations` to identify the specific stale node.

## Resolving Tribunal Backlogs
1. Use `preview-context-dispute-tribunals`.
2. If cases are stuck in `case_collecting_evidence`, verify the Evidence Atlas connection.
3. If cases are stuck in `case_quorum_pending`, check `tribunal_quorum_and_evidence_rules` in config.

## Fixing Degraded Broker Exchanges
1. Use `preview-broker-exchanges`.
2. Check if routes are defaulting to `routed_caveated_exchange` due to `incomplete_evidence`.
3. Review `broker_exchange_fairness_rules` if fairness metrics are dropping below acceptable thresholds.
