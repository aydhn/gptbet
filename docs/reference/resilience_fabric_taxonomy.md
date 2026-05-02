# Resilience Fabric Taxonomy

## Relays
- `external_catalog_relay`
- `trust_signal_relay`
- `mirror_health_relay`
- ...

## Swarms
- `registry_mirror_swarm`
- `checkpoint_mirror_swarm`
- ...

## Strategies
- `ConservativeResilienceStrategy`: Default. Heavily penalizes divergence, restricts calibration.
- `BalancedRelaySwarmStrategy`: Balanced approach.
- `GameDayFirstResilienceStrategy`: Focuses heavily on resilience scorecards.
- `SwarmStrictConsensusStrategy`: High sensitivity to split-brains.
- `CalibrationGuardedStrategy`: Extremely cautious with trust calibration adjustments.
