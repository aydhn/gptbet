# Hardening Pack 15 Runbook

## Execution
Run the planetary federation hardening validation via the CLI:
```bash
python -m sports_signal_bot.main run-hardening-pack-15
```

## Preview Artifacts
- `python -m sports_signal_bot.main preview-planetary-mesh-federation-report`
- `python -m sports_signal_bot.main preview-corridor-superchain-report`
- `python -m sports_signal_bot.main preview-scheduler-bus-report`
- `python -m sports_signal_bot.main preview-audit-cadence-report`
- `python -m sports_signal_bot.main preview-planetary-federation-hardening-health`

## Remediation
If warnings exist:
1. Identify the source of the blocked/caveated federation (stale nodes vs missing lineage).
2. For missing Acks in Cadence, verify the scheduler bus route.
3. For broken superchains, confirm source/target hash viability.
