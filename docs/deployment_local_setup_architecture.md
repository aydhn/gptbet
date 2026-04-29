# Deployment Local Setup Architecture

## Why Portable Local Deployment Matters
Our system is a complex sports forecasting ecosystem. To ensure reliability, we must be able to bootstrap, backup, and restore the environment deterministically on any local machine, without relying on Docker or cloud infrastructure.

## Workspace Layout
- `config/`: Configuration files
- `data/`: Raw/interim/processed datasets
- `artifacts/`: Models and manifests
- `state/`: Locks and local state
- `secrets/`: Local keys (excluded from raw backup)

## Doctor
Runs safety and compatibility checks before any dispatch.

## Future Path
Can be extended for containerization or signed zip releases.
