import pytest
from sports_signal_bot.governance_assurance.contracts import SnapshotState
from sports_signal_bot.governance_assurance.snapshots import (
    capture_dashboard_snapshot, compare_dashboard_snapshots
)
from sports_signal_bot.governance_assurance.alerts import generate_alert_ribbons

def test_capture_and_compare_snapshots():
    snap_current = capture_dashboard_snapshot("s1", "v1", is_stale=False, has_caveats=False)
    assert snap_current.state == SnapshotState.CURRENT

    snap_stale = capture_dashboard_snapshot("s2", "v1", is_stale=True, has_caveats=False)
    assert snap_stale.state == SnapshotState.STALE

    snap_caveat = capture_dashboard_snapshot("s3", "v1", is_stale=False, has_caveats=True)
    assert snap_caveat.state == SnapshotState.CAVEATED

    assert compare_dashboard_snapshots(snap_stale, snap_current) == "staleness_resolved"
    assert compare_dashboard_snapshots(snap_current, snap_caveat) == "caveats_introduced"

def test_generate_alert_ribbons():
    alerts = generate_alert_ribbons(["system failure", "stale data", "minor warning"])
    assert len(alerts) == 3
    assert alerts[0].severity == "high"
    assert alerts[1].severity == "high"
    assert alerts[2].severity == "medium"
