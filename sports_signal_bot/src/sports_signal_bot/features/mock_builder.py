import pandas as pd
from typing import List
from .interfaces import BaseFeatureBuilder

class MockFeatureBuilder(BaseFeatureBuilder):
    def build_features(self, events: List[dict]) -> pd.DataFrame:
        # Just a mock transformation
        df = pd.DataFrame(events)
        if len(df) > 0:
            df["mock_f1"] = 1.0
            df["mock_f2"] = 0.5
        return df
