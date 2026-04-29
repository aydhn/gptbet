import os
import json
import shutil
import zipfile
from pathlib import Path
from datetime import datetime
from .contracts import DeploymentLayoutRecord, BackupManifestRecord, BackupType
from .locks import block_conflicting_operation, release_workspace_lock

def create_backup(layout: DeploymentLayoutRecord, btype: BackupType, exclude: list = None) -> BackupManifestRecord:
    block_conflicting_operation(layout.state_root, "backup")
    try:
        manifest = BackupManifestRecord(backup_type=btype, excluded_families=exclude or [])
        backup_name = f"ssb_backup_{manifest.backup_id}_{datetime.now().strftime('%Y%md%H%M%S')}"
        archive_path = Path(layout.backups_root) / backup_name

        # Build the backup zip
        Path(layout.backups_root).mkdir(exist_ok=True, parents=True)
        zip_path = f"{archive_path}.zip"

        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            if btype in [BackupType.CONFIG_AND_STATE_BACKUP, BackupType.FULL_LOCAL_BUNDLE_BACKUP]:
                # Add configs
                if Path(layout.config_root).exists():
                    for root, dirs, files in os.walk(layout.config_root):
                        for file in files:
                            file_path = Path(root) / file
                            arcname = file_path.relative_to(layout.workspace_root)
                            zf.write(file_path, arcname)
                # Add state
                if Path(layout.state_root).exists():
                     for root, dirs, files in os.walk(layout.state_root):
                        for file in files:
                            # Avoid backing up locks
                            if not file.endswith(".lock"):
                                file_path = Path(root) / file
                                arcname = file_path.relative_to(layout.workspace_root)
                                zf.write(file_path, arcname)

        manifest.size_bytes = os.path.getsize(zip_path) if Path(zip_path).exists() else 0

        # Save manifest
        (Path(layout.backups_root) / f"{backup_name}_manifest.json").write_text(manifest.model_dump_json(indent=2))

        return manifest
    finally:
        release_workspace_lock(layout.state_root)
