from datetime import datetime, timezone
from typing import Dict, List, Optional
from sports_signal_bot.monitoring.contracts import FreshnessRecord

def get_now() -> datetime:
    """Helper to get current UTC time."""
    return datetime.now(timezone.utc)

def compute_age_minutes(last_updated: datetime, now: Optional[datetime] = None) -> float:
    """Compute age in minutes from last_updated to now."""
    if now is None:
        now = get_now()
    if last_updated.tzinfo is None:
        last_updated = last_updated.replace(tzinfo=timezone.utc)
    if now.tzinfo is None:
        now = now.replace(tzinfo=timezone.utc)
    delta = now - last_updated
    return max(0.0, delta.total_seconds() / 60.0)

def compute_age_hours(last_updated: datetime, now: Optional[datetime] = None) -> float:
    return compute_age_minutes(last_updated, now) / 60.0

def compute_age_days(last_updated: datetime, now: Optional[datetime] = None) -> float:
    return compute_age_hours(last_updated, now) / 24.0

def evaluate_freshness_against_threshold(
    entity_name: str,
    entity_type: str,
    last_updated: datetime,
    threshold_minutes: float,
    now: Optional[datetime] = None
) -> FreshnessRecord:
    age_minutes = compute_age_minutes(last_updated, now)
    is_stale = age_minutes > threshold_minutes
    return FreshnessRecord(
        entity_name=entity_name,
        entity_type=entity_type,
        last_updated=last_updated,
        age_minutes=age_minutes,
        is_stale=is_stale,
        stale_threshold_minutes=threshold_minutes
    )

def summarize_stale_entities(records: List[FreshnessRecord]) -> Dict[str, int]:
    summary = {}
    for record in records:
        if record.is_stale:
            summary[record.entity_type] = summary.get(record.entity_type, 0) + 1
    return summary

def detect_stale_chain_components(records: List[FreshnessRecord]) -> List[str]:
    return [r.entity_name for r in records if r.is_stale]
