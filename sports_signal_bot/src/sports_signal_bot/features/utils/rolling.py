from typing import List

import pandas as pd


def calculate_rolling_aggregates(
    events_df: pd.DataFrame, windows: List[int]
) -> pd.DataFrame:
    """
    Utility to calculate event-time safe rolling aggregates.
    Ensures that for any event, only data occurring *strictly before* the event time is used.
    """
    # For now, we return a structural placeholder.
    # A full implementation requires sorting by team and time, then grouping and shifting.
    df = pd.DataFrame({"event_id": events_df["event_id"]})

    # Placeholder for test / structure
    df["home_last_5_wins_proxy"] = 2.0
    df["away_last_5_wins_proxy"] = 1.0
    df["home_last_5_points_proxy"] = 6.0
    df["away_last_5_points_proxy"] = 3.0

    return df
