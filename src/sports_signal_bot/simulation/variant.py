from .contracts import VariantSnapshotRecord
import uuid

def build_variant_snapshot(request_id: str, data: dict) -> VariantSnapshotRecord:
    return VariantSnapshotRecord(
        snapshot_id=f"var_{uuid.uuid4().hex[:8]}",
        metrics=data.get("metrics", {}),
        decision_counts=data.get("decision_counts", {})
    )
