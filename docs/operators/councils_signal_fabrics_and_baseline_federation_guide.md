# Operator Guide: Councils, Signal Fabrics, and Baseline Federation

## Governance Fabric Execution
To manually trigger the governance fabric adjudication and flow processes, run:
```bash
python -m sports_signal_bot.main governance-fabric run-governance-fabric-pass
```

This will output a summary to `results/governance_fabric_summary.json` containing the outcomes of council cases, signal flows, federated baseline projections, and audit replays.

## Monitoring the Fabric
You can inspect individual components using the preview commands:
*   `preview-governance-councils`: Check council health and active cases.
*   `preview-signal-fabrics`: Monitor flow success rates and suppression events due to pressure.
*   `preview-baseline-federations`: Verify if federated baselines are projecting as current or stale.
*   `preview-projection-audit-exchanges`: See the validity rate of incoming audit packets.

## Handling Fabric Pressure
If `preview-signal-fabrics` shows high pressure (e.g., `suppress_noncritical_signal_paths`), the fabric is detecting too many stale or conflicting signals. The system will automatically suppress flows, but operators should investigate the underlying signal sources for degradation.
