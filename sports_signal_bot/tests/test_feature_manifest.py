import os

import pandas as pd
import pytest

from sports_signal_bot.features.builders.context import ContextFeatureBuilder
from sports_signal_bot.features.contracts import FeatureBuildContext
from sports_signal_bot.features.manifests import generate_manifest


def test_generate_manifest(tmp_path):
    context = FeatureBuildContext(sport="football", run_id="test_run")
    events_df = pd.DataFrame({"event_id": ["e1"]})
    matrix_df = pd.DataFrame({"event_id": ["e1"], "col1": [1]})

    out_path = str(tmp_path / "test")

    manifest = generate_manifest(
        context=context,
        data={"events": events_df},
        feature_matrix=matrix_df,
        active_builders=[ContextFeatureBuilder()],
        output_path=out_path,
    )

    assert manifest.run_id == "test_run"
    assert manifest.row_count == 1
    assert "col1" in manifest.produced_columns
    assert os.path.exists(out_path + ".manifest.json")
