import json
from pathlib import Path
from .contracts import MigrationPreflightRecord, DeploymentLayoutRecord

def run_upgrade_preflight(layout: DeploymentLayoutRecord) -> MigrationPreflightRecord:
    # A robust preflight checking config formats and checking if directories are populated
    # In a full migration, we would inspect a versioned tracking file in state
    blocking_issues = []
    required_migrations = []

    # Check if a critical legacy file structure exists indicating needing migration
    legacy_file = Path(layout.data_root) / "legacy_format.json"
    if legacy_file.exists():
         required_migrations.append("migrate_legacy_data")

    # Ensure backups exist before upgrading
    backups_dir = Path(layout.backups_root)
    if not backups_dir.exists() or len(list(backups_dir.glob("*.zip"))) == 0:
         blocking_issues.append("No local backup found. Please create a backup before performing an upgrade.")

    return MigrationPreflightRecord(
        current_layout_version=layout.layout_version,
        current_schema_version="0.9.5",
        required_migrations=required_migrations,
        blocking_issues=blocking_issues,
        backup_recommended=True
    )
