from typing import List, Dict, Any
from datetime import datetime
from .contracts import RegistrySnapshotRecord

def build_registry_snapshot(
    snapshot_id: str,
    registry_id: str,
    signed_snapshot_manifest: str,
    exported_artifact_list: List[str]
) -> RegistrySnapshotRecord:
    """Builds a new registry snapshot."""
    return RegistrySnapshotRecord(
        snapshot_id=snapshot_id,
        registry_id=registry_id,
        signed_snapshot_manifest=signed_snapshot_manifest,
        exported_artifact_list=exported_artifact_list,
        validity="valid"
    )

def export_registry_snapshot(snapshot: RegistrySnapshotRecord) -> Dict[str, Any]:
    return snapshot.model_dump()

def import_registry_snapshot(data: Dict[str, Any]) -> RegistrySnapshotRecord:
    return RegistrySnapshotRecord(**data)

def compare_snapshots_for_drift(local_snapshot: RegistrySnapshotRecord, remote_snapshot: RegistrySnapshotRecord) -> List[str]:
    drift = []
    if len(local_snapshot.exported_artifact_list) != len(remote_snapshot.exported_artifact_list):
        drift.append("Artifact count mismatch")
    return drift

def summarize_sync_state(snapshots: List[RegistrySnapshotRecord]) -> Dict[str, Any]:
    return {
        "total_snapshots": len(snapshots)
    }
