from datetime import datetime
from typing import Dict, Any
from .contracts import SyncLagRecord, SyncCheckpointRecord

def compute_sync_lag(checkpoint: SyncCheckpointRecord, current_time: datetime) -> SyncLagRecord:
    """Computes the lag between a checkpoint and current time."""
    lag_seconds = int((current_time - checkpoint.local.timestamp).total_seconds())
    is_stale = lag_seconds > 86400 # 1 day default threshold for demo

    return SyncLagRecord(
        lag_id=f"lag_{checkpoint.checkpoint_id}",
        subscription_id=checkpoint.source.source_ref, # Simplification
        lag_seconds=lag_seconds,
        is_stale=is_stale
    )

def summarize_sync_lag(lag_records: list[SyncLagRecord]) -> Dict[str, Any]:
    """Summarizes lag statistics across multiple records."""
    if not lag_records:
        return {"avg_lag_seconds": 0, "max_lag_seconds": 0, "stale_count": 0}

    lags = [r.lag_seconds for r in lag_records]
    return {
        "avg_lag_seconds": sum(lags) / len(lags),
        "max_lag_seconds": max(lags),
        "stale_count": sum(1 for r in lag_records if r.is_stale)
    }
