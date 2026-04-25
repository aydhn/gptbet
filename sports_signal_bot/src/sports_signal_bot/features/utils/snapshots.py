import pandas as pd

from sports_signal_bot.core.logger import get_logger

logger = get_logger("SnapshotUtils")


def select_feature_snapshot(
    events_df: pd.DataFrame, odds_df: pd.DataFrame, policy: str
) -> pd.DataFrame:
    """
    Selects the most appropriate pre-match odds snapshot, avoiding post-event leakage.
    Returns a DataFrame keyed by event_id.
    """
    if (
        odds_df.empty
        or "snapshot_time_utc" not in odds_df.columns
        or "event_datetime_utc" not in events_df.columns
    ):
        return odds_df.copy()

    merged = pd.merge(
        odds_df,
        events_df[["event_id", "event_datetime_utc"]],
        on="event_id",
        how="inner",
    )

    # Ensure snapshot is strictly before event time
    merged["snapshot_dt"] = pd.to_datetime(merged["snapshot_time_utc"], utc=True)
    merged["event_dt"] = pd.to_datetime(merged["event_datetime_utc"], utc=True)

    valid_snapshots = merged[merged["snapshot_dt"] < merged["event_dt"]].copy()

    if len(valid_snapshots) < len(odds_df):
        logger.warning(
            f"Filtered out {len(odds_df) - len(valid_snapshots)} post-event odds snapshots to prevent leakage."
        )

    # Sort by snapshot time and take the latest valid one per event/market/bookmaker
    # For feature matrix, we usually want consensus or a specific bookmaker,
    # here we assume the calling builder will aggregate or we just return the latest overall valid one.
    valid_snapshots = valid_snapshots.sort_values("snapshot_dt", ascending=False)
    latest_valid = valid_snapshots.groupby("event_id").first().reset_index()

    # Clean up temporary columns
    return latest_valid.drop(
        columns=["snapshot_dt", "event_dt", "event_datetime_utc"], errors="ignore"
    )
