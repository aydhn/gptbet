from typing import Dict, List, Any
import datetime
from .contracts import StableReferenceSnapshotRecord

def capture_stable_reference_snapshot(adoption_id: str, stable_pointers: Dict[str, str], manifest_refs: List[str]) -> StableReferenceSnapshotRecord:
    return StableReferenceSnapshotRecord(
        snapshot_id=f"snap_{datetime.datetime.now(datetime.timezone.utc).timestamp()}",
        adoption_id=adoption_id,
        stable_pointers=stable_pointers,
        manifest_refs=manifest_refs
    )

def validate_snapshot_completeness(snapshot: StableReferenceSnapshotRecord) -> bool:
    return bool(snapshot.stable_pointers and snapshot.manifest_refs)

def store_snapshot_for_rollback(snapshot: StableReferenceSnapshotRecord, storage: Dict[str, StableReferenceSnapshotRecord]) -> None:
    storage[snapshot.snapshot_id] = snapshot

def render_snapshot_summary(snapshot: StableReferenceSnapshotRecord) -> str:
    pointers = ", ".join([f"{k}: {v}" for k, v in snapshot.stable_pointers.items()])
    return f"Snapshot {snapshot.snapshot_id} captured at {snapshot.captured_at} with pointers: {pointers}"
