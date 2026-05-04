from datetime import datetime, timezone
from typing import List
from sports_signal_bot.governance_assurance.contracts import (
    DashboardSnapshotRecord,
    SnapshotState
)

def capture_dashboard_snapshot(
    snapshot_id: str,
    view_ref: str,
    is_stale: bool,
    has_caveats: bool
) -> DashboardSnapshotRecord:

    state = SnapshotState.CURRENT
    if is_stale:
        state = SnapshotState.STALE
    elif has_caveats:
        state = SnapshotState.CAVEATED

    return DashboardSnapshotRecord(
        snapshot_id=snapshot_id,
        view_ref=view_ref,
        state=state,
        timestamp=datetime.now(timezone.utc).isoformat()
    )

def compare_dashboard_snapshots(old_snap: DashboardSnapshotRecord, new_snap: DashboardSnapshotRecord) -> str:
    if old_snap.state == SnapshotState.STALE and new_snap.state == SnapshotState.CURRENT:
        return "staleness_resolved"
    if old_snap.state != SnapshotState.CAVEATED and new_snap.state == SnapshotState.CAVEATED:
        return "caveats_introduced"
    return "stable"
