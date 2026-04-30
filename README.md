# Sports Signal Bot

A modular, extensible sports forecasting system.

## Documentation
The system documentation is organized for operational readiness.

Start here:
- **[Operations Handbook Overview](docs/operations_handbook_overview.md)**

Quick links:
- [Operator Handbook](docs/operators/operator_handbook.md)
- [Incident Playbooks](docs/incidents/stale_artifacts.md)
- [Getting Started / Onboarding](docs/onboarding/getting_started.md)
- [CLI Reference](docs/reference/cli_reference.md)

## Development
See the documentation for architecture and guidelines. Run `python -m sports_signal_bot.main --help` for available commands.

# Phase 36: Platform Packaging & Portable Local Deployment

This phase implements the platform packaging and local deployment automation for the Sports Signal Bot. The focus is on predictability, deterministic bootstrapping, robust environment checking, and safe backup/restore capabilities. It aims to transform the system from a repository into a safely bootstrappable local application.

Key features added:
- **Workspace Layout Standard**: Hard-coded paths are avoided. Roots (config, data, artifacts, logs, etc.) are deterministically generated and centrally managed via `DeploymentLayoutRecord`.
- **Bootstrapping**: `deploy bootstrap` initializes the directory structure and templates missing env/config files based on customizable install profiles (`research_local`, `conservative_ops`).
- **Environment Doctor**: `deploy run-doctor` performs critical readiness checks for Python runtime version, required directories, schemas, and configurations. It reports blocking issues versus warnings and ensures dispatch readiness.
- **First-Class Backup & Restore**: Safe mechanisms to archive configurations, state, and specific metadata while adhering to basic locks and overwrite safety measures to ensure local reproducibility.
- **Upgrade Preflight**: `deploy run-upgrade-preflight-command` to report layout and schema version changes before executing risky structural upgrades.

All implementation details live under `src/sports_signal_bot/deployment` and have corresponding entry points via the `sports_signal_bot.main` Typer app under the `deploy` sub-command.

## Örnek CLI Komutları
```bash
python -m sports_signal_bot.main deploy bootstrap --profile research_local
python -m sports_signal_bot.main deploy run-doctor
python -m sports_signal_bot.main deploy preview-layout
python -m sports_signal_bot.main deploy create-backup-cmd --btype config_and_state_backup
python -m sports_signal_bot.main deploy restore-backup <BACKUP_ID> --dry-run
python -m sports_signal_bot.main deploy run-upgrade-preflight-command
```

# Phase 38: Provider Abstraction Layer

This phase implements a robust Provider Abstraction Layer. It transforms the system from relying on scattered, hard-coded integrations into a unified, contract-driven architecture.

Key features added:
- **Unified Contracts**: Request and response models (`ProviderRequestRecord`, `ProviderResponseRecord`) decouple the inference, monitoring, and reporting layers from provider-specific structures.
- **Provider Registry**: Adapters are dynamically registered (`ProviderRegistry`), making it easy to swap implementations without changing business logic.
- **Failover Engine**: Configurable fallback strategies (e.g., if a remote API fails, fall back to a local mirror or manual dropzone) ensure continuous operation.
- **Quality Scoring**: Responses are no longer just accepted; they are scored based on freshness, completeness, schema validity, and consistency, determining whether a payload is acceptable or if a failover is required.
- **Identity Normalization**: Resolves aliases and normalizes event IDs internally to ensure consistency regardless of the source.

## Reconciliation & Arbiter Layer (Phase 39)
The `reconciliation` module builds on top of the provider abstraction layer to provide a multi-source reconciliation, consensus and arbitration engine. It groups conflicting data across different sources, assigns dynamic trust values, resolves fields via customizable strategies (e.g. `balanced_consensus`, `conservative_truth`), and returns a `TrustedUnifiedRecord`. Unresolvable anomalies escalate via `DisputeRecord`.

Key concepts:
- **Grouping**: Observations are grouped by `entity_key` and normalized.
- **Conflicts**: Field-level contradictions are identified, grouped and graded by severity (e.g. `low`, `critical`).
- **Trust & Confidence**: The output is not a blind average but a strategy-derived consensus alongside a calculated `confidence_score`.
- **Lineage**: Full decision lineage explains how each field's final value was chosen.
- **Commands**: Run reconciliation via CLI (e.g. `python -m sports_signal_bot.main reconciliation run --sport football --family fixtures`).
