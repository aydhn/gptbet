# Witness Mesh Runbook

## Routine Maintenance
- Run `python -m sports_signal_bot.main witness-mesh run-witness-mesh-pass` daily.
- Review `preview-public-style-readiness` weekly.

## Troubleshooting
- **Low Readiness Score**: Check for open challenges or a drop in active witness nodes.
- **Split Consensus**: Investigate the specific `target_ref`. One witness may be reading from a stale mirror.
