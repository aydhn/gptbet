import pytest
import pandas as pd
from sports_signal_bot.evaluation.alignment import align_predictions_to_common_universe

def test_same_sample_policy_empty_intersection():
    df = pd.DataFrame({
        "event_id": ["e1", "e2"],
        "source_name": ["A", "B"]
    })

    aligned, _ = align_predictions_to_common_universe(df)
    assert len(aligned) == 0
