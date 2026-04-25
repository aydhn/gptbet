from typing import List

from sports_signal_bot.ratings.contracts import RatingSnapshotRecord


def extract_snapshots_for_events(
    snapshots: List[RatingSnapshotRecord], event_ids: List[str]
) -> List[RatingSnapshotRecord]:
    target_set = set(event_ids)
    return [s for s in snapshots if s.event_id in target_set]
