# Simulation Runbook

## Running a Simulation
```bash
python -m sports_signal_bot.main simulate-suggestion --suggestion-id <id>
```

## Previewing Strategies
```bash
python -m sports_signal_bot.main list-simulation-strategies
```

## Cleaning up the Sandbox
The system uses the `simulation_cleanup_policy` (default: keep_manifests_only) to ensure disks don't fill up with historical variant replays.
