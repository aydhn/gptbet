from .contracts import BaselineSnapshotRecord
import uuid

def build_baseline_snapshot(request_id: str, data: dict) -> BaselineSnapshotRecord:
    return BaselineSnapshotRecord(
        snapshot_id=f"base_{uuid.uuid4().hex[:8]}",
        metrics=data.get("metrics", {}),
        decision_counts=data.get("decision_counts", {})
    )
