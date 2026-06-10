from datetime import datetime, timezone

from .contracts import (
    LocalSyncCheckpointRecord,
    SourceSyncCheckpointRecord,
    SyncCheckpointRecord,
    SyncHealthRecord,
    SyncStalenessRecord,
)


def create_sync_checkpoint(
    source_ref: str, local_ref: str, source_digest: str, local_digest: str
) -> SyncCheckpointRecord:
    """Creates a checkpoint marking the state of a sync."""
    now = datetime.now(timezone.utc)
    return SyncCheckpointRecord(
        checkpoint_id=f"chk_{now.timestamp()}",
        source=SourceSyncCheckpointRecord(
            source_ref=source_ref, last_seen_digest=source_digest, timestamp=now
        ),
        local=LocalSyncCheckpointRecord(
            local_ref=local_ref, last_synced_digest=local_digest, timestamp=now
        ),
    )


def detect_stale_subscriptions(
    checkpoints: list[SyncCheckpointRecord], threshold_seconds: int
) -> list[SyncStalenessRecord]:
    """Detects which subscriptions are stale based on their checkpoints."""
    now = datetime.now(timezone.utc)
    results = []
    for chk in checkpoints:
        lag = (now - chk.local.timestamp).total_seconds()
        is_stale = lag > threshold_seconds
        results.append(
            SyncStalenessRecord(
                staleness_id=f"stale_{chk.checkpoint_id}", is_stale=is_stale
            )
        )
    return results


def classify_sync_health(
    staleness_records: list[SyncStalenessRecord],
) -> SyncHealthRecord:
    """Classifies overall sync health based on staleness records."""
    stale_count = sum(1 for r in staleness_records if r.is_stale)
    status = "healthy"
    if stale_count > 0:
        status = "degraded" if stale_count < len(staleness_records) else "unhealthy"

    return SyncHealthRecord(
        health_id=f"health_{datetime.now(timezone.utc).timestamp()}",
        status=status,
        stale_count=stale_count,
    )
