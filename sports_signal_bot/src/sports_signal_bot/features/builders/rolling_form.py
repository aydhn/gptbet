import pandas as pd
from typing import Dict, List
from sports_signal_bot.features.base import BaseFeatureBuilder
from sports_signal_bot.features.contracts import FeatureBuildContext
from sports_signal_bot.features.utils.rolling import calculate_rolling_aggregates

class RollingFormFeatureBuilder(BaseFeatureBuilder):
    """Calculates generic rolling form aggregations (e.g., points, wins)."""

    @property
    def name(self) -> str:
        return "rolling_form"

    @property
    def family(self) -> str:
        return "recent_form"

    @property
    def supported_sports(self) -> List[str]:
        return ["all"]

    @property
    def required_inputs(self) -> List[str]:
        return ["events"]

    @property
    def output_columns(self) -> List[str]:
        return [
            "home_last_5_wins_proxy", "away_last_5_wins_proxy",
            "home_last_5_points_proxy", "away_last_5_points_proxy"
        ]

    def build(self, context: FeatureBuildContext, data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        events_df = data["events"].copy()
        if "event_id" not in events_df.columns:
            return pd.DataFrame(columns=["event_id"] + self.output_columns)

        # This is a stub calling the rolling util that will be built in step 6.
        # We pass it to the util to handle event-time safe sorting and aggregation.
        df = calculate_rolling_aggregates(events_df, context.lookback_windows)

        # Ensure only expected columns + event_id are returned
        cols = ["event_id"] + [c for c in self.output_columns if c in df.columns]

        # Fill missing expected columns with None for now
        for col in self.output_columns:
            if col not in cols:
                df[col] = None
                cols.append(col)

        return df[cols]
