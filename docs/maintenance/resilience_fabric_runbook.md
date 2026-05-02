# Resilience Fabric Runbook

## Commands
Run the full pass (bridging, swarm eval, calibration, game-days):
```bash
python -m sports_signal_bot.main run-resilience-fabric-pass
```

Preview current external relays:
```bash
python -m sports_signal_bot.main preview-external-relays
```

Preview simulation results:
```bash
python -m sports_signal_bot.main preview-game-day-simulations
```

## Degraded Mode
If the system enters a recovery mode due to relay instability, manual intervention might be required to resolve split-brains before exiting the mode.
