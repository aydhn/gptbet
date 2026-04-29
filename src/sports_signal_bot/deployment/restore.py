import os
import zipfile
import logging
from pathlib import Path
from .contracts import DeploymentLayoutRecord
from .locks import block_conflicting_operation, release_workspace_lock

def run_restore(layout: DeploymentLayoutRecord, backup_id: str, dry_run: bool = False, force: bool = False):
    block_conflicting_operation(layout.state_root, "restore")
    try:
        results = {"status": "success", "restored_files": [], "warnings": []}
        backup_dir = Path(layout.backups_root)

        # Find backup archive
        archives = list(backup_dir.glob(f"*{backup_id}*.zip"))
        if not archives:
            raise FileNotFoundError(f"Backup {backup_id} not found.")

        archive = archives[0]
        if dry_run:
            with zipfile.ZipFile(archive, 'r') as zf:
                results["restored_files"] = zf.namelist()
            results["status"] = "dry-run success"
        else:
            if not force:
                raise RuntimeError("Restore operation requires confirmation (force=True) to prevent accidental overwrites.")

            # Perform cautious restore by iterating files
            with zipfile.ZipFile(archive, 'r') as zf:
                for member in zf.infolist():
                    target_path = Path(layout.workspace_root) / member.filename

                    if target_path.exists() and not force:
                         results["warnings"].append(f"Skipped {member.filename} (already exists)")
                         continue

                    # Extract single file/directory
                    zf.extract(member, layout.workspace_root)
                    results["restored_files"].append(member.filename)

        return results
    finally:
        release_workspace_lock(layout.state_root)
