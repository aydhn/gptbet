import pytest
import datetime
from sports_signal_bot.concurrency_hardening.stale_reads import capture_freshness_snapshot, compare_read_versions, detect_consistency_drift
from sports_signal_bot.concurrency_hardening.contracts import FreshnessSnapshotRecord, StaleReadRecord

def test_capture_freshness_snapshot():
    snapshot = capture_freshness_snapshot()
    assert snapshot is not None

def test_compare_read_versions():
    ts = datetime.datetime.now(datetime.timezone.utc)
    snapshot = FreshnessSnapshotRecord(snapshot_id="snap1", timestamp=ts)
    current = ts + datetime.timedelta(milliseconds=500)

    # 600ms > 500ms -> no violation
    assert compare_read_versions(snapshot, current, 600) is None
    # 400ms < 500ms -> violation
    violation = compare_read_versions(snapshot, current, 400)
    assert violation is not None
    assert violation.drift_ms >= 500
