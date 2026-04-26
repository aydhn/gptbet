import pandas as pd
import pytest

from sports_signal_bot.evaluation.alignment import (
    align_predictions_to_common_universe,
    get_common_universe,
)


def test_common_universe_alignment():
    df = pd.DataFrame(
        {
            "event_id": ["e1", "e2", "e3", "e1", "e2"],
            "source_name": ["A", "A", "A", "B", "B"],
        }
    )

    aligned_df, counts = align_predictions_to_common_universe(df)

    assert counts["A"] == 3
    assert counts["B"] == 2

    # Event e3 is only in A, so it should be dropped
    assert "e3" not in aligned_df["event_id"].values
    assert len(aligned_df) == 4

    # Test skipping alignment
    aligned_df2, _ = align_predictions_to_common_universe(df, same_sample_only=False)
    assert len(aligned_df2) == 5
