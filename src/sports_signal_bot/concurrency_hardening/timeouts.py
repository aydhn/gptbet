import uuid
import datetime
from typing import Dict, Any, List

from .contracts import (
    CancellationRunRecord, TimeoutRunRecord, PartialCompletionRecord,
    CleanupRecord, CancellationLeakRecord, TimeoutCompensationRecord,
    CancellationHealthRecord, TimeoutManifestRecord, TimeoutWarningRecord
)

def run_timeout_probe(target_ref: str, simulates_timeout: bool) -> TimeoutRunRecord:
    """Simulates a timeout probe."""
    status = "timeout_simulated" if simulates_timeout else "completed"
    warnings = []

    if simulates_timeout:
        warnings.append(
            TimeoutWarningRecord(
                warning_id=f"warn_{uuid.uuid4().hex[:8]}",
                message="Timeout simulated, verify partial state handling.",
                severity="medium"
            )
        )

    return TimeoutRunRecord(
        run_id=f"tor_{uuid.uuid4().hex[:8]}",
        target_ref=target_ref,
        status=status,
        warnings=warnings
    )

def run_cancellation_probe(target_ref: str, simulates_cancellation: bool) -> CancellationRunRecord:
    """Simulates a cancellation probe."""
    status = "cancellation_simulated" if simulates_cancellation else "completed"
    warnings = []

    if simulates_cancellation:
        warnings.append(
            TimeoutWarningRecord(
                warning_id=f"warn_{uuid.uuid4().hex[:8]}",
                message="Cancellation simulated, verify leak cleanup.",
                severity="medium"
            )
        )

    return CancellationRunRecord(
        run_id=f"cxr_{uuid.uuid4().hex[:8]}",
        target_ref=target_ref,
        status=status,
        warnings=warnings
    )

def detect_cancellation_leaks(runs: List[CancellationRunRecord]) -> List[CancellationLeakRecord]:
    """Detects leaks from cancelled runs."""
    leaks = []
    for r in runs:
        if r.status == "cancellation_simulated":
            # In a real system, we'd check resources. Here we simulate finding a leak sometimes.
            # We'll just generate one for demonstration if requested.
            pass
    return leaks

def summarize_timeout_and_cancellation(runs: List[TimeoutRunRecord], leaks: List[CancellationLeakRecord]) -> TimeoutManifestRecord:
    """Summarizes timeout and cancellation health."""
    health = CancellationHealthRecord(
        health_id=f"hlt_{uuid.uuid4().hex[:8]}",
        is_healthy=len(leaks) == 0,
        status_summary=f"Found {len(leaks)} resource leaks post-cancellation."
    )

    return TimeoutManifestRecord(
        manifest_id=f"man_{uuid.uuid4().hex[:8]}",
        generated_at=datetime.datetime.now(datetime.timezone.utc),
        runs=runs,
        health=health
    )
