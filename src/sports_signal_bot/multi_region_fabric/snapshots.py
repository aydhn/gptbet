from datetime import datetime, timezone
from sports_signal_bot.multi_region_fabric.contracts import RegionSnapshotRecord

def build_region_snapshot(region_id: str) -> RegionSnapshotRecord:
    return RegionSnapshotRecord(
        snapshot_id=f"snap_{region_id}_{int(datetime.now(timezone.utc).timestamp())}",
        region_id=region_id,
        timestamp=datetime.now(timezone.utc),
        hash_ref="hash_123"
    )

def validate_snapshot_freshness_for_transfer(snap: RegionSnapshotRecord) -> bool:
    return True

def compare_region_snapshots(s1: RegionSnapshotRecord, s2: RegionSnapshotRecord) -> bool:
    return s1.hash_ref == s2.hash_ref

def summarize_snapshot_transfer_state(snap: RegionSnapshotRecord) -> str:
    return f"Snapshot {snap.snapshot_id} ready"
