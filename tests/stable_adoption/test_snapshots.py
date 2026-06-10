import pytest
import datetime
from unittest.mock import patch
from sports_signal_bot.stable_adoption.snapshots import (
    capture_stable_reference_snapshot,
    validate_snapshot_completeness,
    store_snapshot_for_rollback,
    render_snapshot_summary,
)
from sports_signal_bot.stable_adoption.contracts import StableReferenceSnapshotRecord

def test_capture_stable_reference_snapshot():
    adoption_id = "ad_123"
    stable_pointers = {"pointer1": "ref1", "pointer2": "ref2"}
    manifest_refs = ["manifest1", "manifest2"]

    with patch("sports_signal_bot.stable_adoption.snapshots.datetime") as mock_datetime:
        mock_now = datetime.datetime(2023, 1, 1, 12, 0, 0, tzinfo=datetime.timezone.utc)
        mock_datetime.datetime.now.return_value = mock_now
        mock_datetime.timezone = datetime.timezone

        snapshot = capture_stable_reference_snapshot(adoption_id, stable_pointers, manifest_refs)

        assert snapshot.snapshot_id.startswith("snap_")
        assert snapshot.adoption_id == adoption_id
        assert snapshot.stable_pointers == stable_pointers
        assert snapshot.manifest_refs == manifest_refs
        # Check that captured_at was set
        assert isinstance(snapshot.captured_at, datetime.datetime)

def test_validate_snapshot_completeness_complete():
    snapshot = StableReferenceSnapshotRecord(
        snapshot_id="snap_123",
        adoption_id="ad_123",
        stable_pointers={"p1": "r1"},
        manifest_refs=["m1"]
    )
    assert validate_snapshot_completeness(snapshot) is True

def test_validate_snapshot_completeness_incomplete_pointers():
    snapshot = StableReferenceSnapshotRecord(
        snapshot_id="snap_123",
        adoption_id="ad_123",
        stable_pointers={},
        manifest_refs=["m1"]
    )
    assert validate_snapshot_completeness(snapshot) is False

def test_validate_snapshot_completeness_incomplete_manifests():
    snapshot = StableReferenceSnapshotRecord(
        snapshot_id="snap_123",
        adoption_id="ad_123",
        stable_pointers={"p1": "r1"},
        manifest_refs=[]
    )
    assert validate_snapshot_completeness(snapshot) is False

def test_store_snapshot_for_rollback():
    snapshot = StableReferenceSnapshotRecord(
        snapshot_id="snap_123",
        adoption_id="ad_123",
    )
    storage = {}
    store_snapshot_for_rollback(snapshot, storage)

    assert "snap_123" in storage
    assert storage["snap_123"] == snapshot

def test_render_snapshot_summary():
    dt = datetime.datetime(2023, 1, 1, 12, 0, 0, tzinfo=datetime.timezone.utc)
    snapshot = StableReferenceSnapshotRecord(
        snapshot_id="snap_123",
        adoption_id="ad_123",
        stable_pointers={"p1": "r1", "p2": "r2"},
        captured_at=dt
    )

    summary = render_snapshot_summary(snapshot)

    assert "Snapshot snap_123" in summary
    assert "captured at 2023-01-01 12:00:00+00:00" in summary
    assert "pointers: p1: r1, p2: r2" in summary
