import pandas as pd
from typing import List
from sports_signal_bot.ratings.contracts import RatingSnapshotRecord
def snapshots_to_dataframe(snapshots: List[RatingSnapshotRecord]) -> pd.DataFrame:
    if not snapshots: return pd.DataFrame()
    return pd.DataFrame([s.model_dump() for s in snapshots])
def get_snapshot_for_event(snapshots: List[RatingSnapshotRecord], event_id: str) -> RatingSnapshotRecord:
    for s in snapshots:
        if s.event_id == event_id: return s
    raise ValueError(f"Snapshot not found for event_id: {event_id}")
