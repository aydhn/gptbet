from typing import Dict, List, Set, Tuple

import pandas as pd


def get_common_universe(
    df: pd.DataFrame, source_col: str = "source_name", event_id_col: str = "event_id"
) -> Set[str]:
    """Finds the intersection of event_ids present in ALL sources."""
    sources = df[source_col].unique()
    if len(sources) == 0:
        return set()

    common_events = None
    for source in sources:
        source_events = set(df[df[source_col] == source][event_id_col].unique())
        if common_events is None:
            common_events = source_events
        else:
            common_events = common_events.intersection(source_events)

    return common_events if common_events is not None else set()


def align_predictions_to_common_universe(
    df: pd.DataFrame,
    source_col: str = "source_name",
    event_id_col: str = "event_id",
    same_sample_only: bool = True,
) -> Tuple[pd.DataFrame, Dict[str, int]]:
    """Filters dataframe to only include events present in all sources if requested."""

    sources = df[source_col].unique()
    original_counts = {source: len(df[df[source_col] == source]) for source in sources}

    if not same_sample_only or len(sources) <= 1:
        return df.copy(), original_counts

    common_events = get_common_universe(df, source_col, event_id_col)
    aligned_df = df[df[event_id_col].isin(common_events)].copy()

    return aligned_df, original_counts


def summarize_coverage_by_source(
    aligned_df: pd.DataFrame,
    original_counts: Dict[str, int],
    source_col: str = "source_name",
) -> Dict[str, float]:
    """Calculates coverage rate (aligned count / original count) for each source."""
    coverage = {}
    sources = aligned_df[source_col].unique()

    for source in sources:
        aligned_count = len(aligned_df[aligned_df[source_col] == source])
        orig_count = original_counts.get(source, 0)

        if orig_count > 0:
            coverage[source] = aligned_count / orig_count
        else:
            coverage[source] = 0.0

    return coverage
