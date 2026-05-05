import uuid
import datetime
from typing import Dict, Any, List, Optional

from .contracts import (
    StaleReadRecord, FreshnessSnapshotRecord, DriftWindowRecord,
    DriftViolationRecord, DriftCompensationRecord, DriftHealthRecord,
    DriftManifestRecord, DriftWarningRecord
)

def capture_freshness_snapshot() -> FreshnessSnapshotRecord:
    """Captures a freshness snapshot timestamp."""
    return FreshnessSnapshotRecord(
        snapshot_id=f"snap_{uuid.uuid4().hex[:8]}",
        timestamp=datetime.datetime.now(datetime.timezone.utc)
    )

def compare_read_versions(snapshot: FreshnessSnapshotRecord, current_time: datetime.datetime, max_drift_ms: int) -> Optional[DriftViolationRecord]:
    """Compares read versions to detect unacceptable drift."""
    drift_td = current_time - snapshot.timestamp
    drift_ms = int(drift_td.total_seconds() * 1000)

    if drift_ms > max_drift_ms:
        return DriftViolationRecord(
            violation_id=f"viol_{uuid.uuid4().hex[:8]}",
            drift_ms=drift_ms
        )
    return None

def detect_consistency_drift(read_record: StaleReadRecord, violation: Optional[DriftViolationRecord]) -> None:
    """Updates record based on drift violation."""
    if violation:
        read_record.status = "drift_detected"
        read_record.warnings.append(
            DriftWarningRecord(
                warning_id=f"warn_{uuid.uuid4().hex[:8]}",
                message=f"Drift of {violation.drift_ms}ms detected.",
                severity="high"
            )
        )

def summarize_stale_read_risks(records: List[StaleReadRecord]) -> DriftManifestRecord:
    """Summarizes stale read and drift risks."""
    drifts = sum(1 for r in records if r.status == "drift_detected")

    health = DriftHealthRecord(
        health_id=f"hlt_{uuid.uuid4().hex[:8]}",
        is_healthy=drifts == 0,
        status_summary=f"Found {drifts} records with unacceptable drift."
    )

    return DriftManifestRecord(
        manifest_id=f"man_{uuid.uuid4().hex[:8]}",
        generated_at=datetime.datetime.now(datetime.timezone.utc),
        records=records,
        health=health
    )
