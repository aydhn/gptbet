import uuid

from .contracts import (
    FailoverCheckpointFamily,
    FailoverCheckpointRecord,
    FailoverContinuityRecord,
    FailoverDependencyRecord,
    FailoverGapRecord,
    FailoverHealthMarkerRecord,
    FailoverLagWindowRecord,
    FailoverVerificationRecord,
)


def create_failover_checkpoint(
    family: FailoverCheckpointFamily, status: str
) -> FailoverCheckpointRecord:
    return FailoverCheckpointRecord(
        checkpoint_id=str(uuid.uuid4()), family=family, status=status
    )


def detect_failover_gaps(gaps: list[FailoverGapRecord]) -> bool:
    return len(gaps) > 0


def compute_failover_lag_window(windows: list[FailoverLagWindowRecord]) -> int:
    return 0


def summarize_failover_checkpoint_health(
    checkpoints: list[FailoverCheckpointRecord],
) -> str:
    return "healthy"
