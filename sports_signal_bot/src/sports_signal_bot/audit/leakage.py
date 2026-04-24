from typing import List, Optional
from datetime import datetime
from sports_signal_bot.data.contracts.canonical import CanonicalOddsRecord
from sports_signal_bot.results.contracts import EventResultRecord
from sports_signal_bot.labels.contracts import LeakageAuditRecord

def detect_post_event_snapshot_leakage(
    event_start_time_utc: datetime,
    snapshot_ts_utc: datetime,
    event_id: str,
    label_name: str
) -> LeakageAuditRecord:
    if snapshot_ts_utc > event_start_time_utc:
        return LeakageAuditRecord(
            event_id=event_id,
            label_name=label_name,
            audit_status="fail",
            issue_type="post_event_odds_snapshot",
            message=f"Odds snapshot {snapshot_ts_utc} is after event start {event_start_time_utc}"
        )
    return LeakageAuditRecord(
        event_id=event_id,
        label_name=label_name,
        audit_status="pass",
        issue_type="odds_snapshot_timing",
        message="Snapshot is pre-match"
    )

def filter_pre_match_odds_snapshots(
    snapshots: List[CanonicalOddsRecord],
    event_start_time_utc: datetime
) -> List[CanonicalOddsRecord]:
    return [s for s in snapshots if s.snapshot_ts_utc <= event_start_time_utc]

def select_latest_pre_match_snapshot(
    snapshots: List[CanonicalOddsRecord],
    event_start_time_utc: datetime
) -> List[CanonicalOddsRecord]:
    valid = filter_pre_match_odds_snapshots(snapshots, event_start_time_utc)
    if not valid: return []

    # Assuming group by market and bookmaker logic is needed to get the *latest*
    # For now, simple return of the latest by timestamp of the whole set
    latest_ts = max(s.snapshot_ts_utc for s in valid)
    return [s for s in valid if s.snapshot_ts_utc == latest_ts]

def group_odds_by_event_market(snapshots: List[CanonicalOddsRecord]) -> dict:
    grouped = {}
    for s in snapshots:
        key = (s.event_id, s.market_type)
        if key not in grouped:
            grouped[key] = []
        grouped[key].append(s)
    return grouped
