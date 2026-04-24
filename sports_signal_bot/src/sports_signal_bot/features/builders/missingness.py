import pandas as pd
from typing import Dict, List
from sports_signal_bot.features.base import BaseFeatureBuilder
from sports_signal_bot.features.contracts import FeatureBuildContext

class MissingnessFeatureBuilder(BaseFeatureBuilder):
    """Generates features describing data quality/missingness."""

    @property
    def name(self) -> str:
        return "data_missingness"

    @property
    def family(self) -> str:
        return "missingness"

    @property
    def supported_sports(self) -> List[str]:
        return ["all"]

    @property
    def required_inputs(self) -> List[str]:
        return ["events"]

    @property
    def output_columns(self) -> List[str]:
        return [
            "missing_stats_count_proxy", "source_confidence_placeholder"
        ]

    def build(self, context: FeatureBuildContext, data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        events_df = data["events"]
        df = pd.DataFrame({"event_id": events_df["event_id"]})

        # Count missing generic stats if they existed
        df["missing_stats_count_proxy"] = 0
        df["source_confidence_placeholder"] = 1.0

        return df
