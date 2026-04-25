from typing import Dict, List

import pandas as pd

from sports_signal_bot.features.base import BaseFeatureBuilder
from sports_signal_bot.features.contracts import FeatureBuildContext


class RestFeatureBuilder(BaseFeatureBuilder):
    """Calculates rest days and schedule density."""

    @property
    def name(self) -> str:
        return "rest_schedule"

    @property
    def family(self) -> str:
        return "schedule_density"

    @property
    def supported_sports(self) -> List[str]:
        return ["all"]

    @property
    def required_inputs(self) -> List[str]:
        return ["events"]

    @property
    def output_columns(self) -> List[str]:
        return [
            "home_days_since_last_match",
            "away_days_since_last_match",
            "home_short_rest_flag",
            "away_short_rest_flag",
        ]

    def build(
        self, context: FeatureBuildContext, data: Dict[str, pd.DataFrame]
    ) -> pd.DataFrame:
        events_df = data["events"].copy()
        if (
            "event_id" not in events_df.columns
            or "event_datetime_utc" not in events_df.columns
        ):
            df = pd.DataFrame(columns=["event_id"] + self.output_columns)
            if "event_id" in events_df.columns:
                df["event_id"] = events_df["event_id"]
            return df

        # Placeholder logic: in reality, this needs to sort by time per team
        # and calculate diff. We implement a dummy mapping here as structural placeholder.
        df = pd.DataFrame({"event_id": events_df["event_id"]})
        df["home_days_since_last_match"] = 7.0  # placeholder
        df["away_days_since_last_match"] = 7.0  # placeholder
        df["home_short_rest_flag"] = 0
        df["away_short_rest_flag"] = 0

        return df
