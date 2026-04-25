from typing import Dict, List

import pandas as pd

from sports_signal_bot.features.base import BaseFeatureBuilder
from sports_signal_bot.features.contracts import FeatureBuildContext
from sports_signal_bot.features.utils.snapshots import select_feature_snapshot


class MarketOddsFeatureBuilder(BaseFeatureBuilder):
    """Extracts features from odds snapshots (implied prob, overround, etc)."""

    @property
    def name(self) -> str:
        return "market_odds"

    @property
    def family(self) -> str:
        return "market_derived"

    @property
    def supported_sports(self) -> List[str]:
        return ["all"]

    @property
    def required_inputs(self) -> List[str]:
        return ["events", "odds"]  # odds is optional but usually required for this

    @property
    def output_columns(self) -> List[str]:
        return [
            "favorite_implied_prob",
            "underdog_implied_prob",
            "market_overround",
            "is_home_favorite",
        ]

    def build(
        self, context: FeatureBuildContext, data: Dict[str, pd.DataFrame]
    ) -> pd.DataFrame:
        events_df = data["events"]

        if "odds" not in data or data["odds"].empty:
            # Return nulls if no odds data
            df = pd.DataFrame({"event_id": events_df["event_id"]})
            for col in self.output_columns:
                df[col] = None
            return df

        odds_df = data["odds"]

        # Select the safest snapshot using the utility
        safe_odds = select_feature_snapshot(
            events_df, odds_df, context.event_time_cutoff_policy
        )

        # Merge and calculate
        df = pd.merge(events_df[["event_id"]], safe_odds, on="event_id", how="left")

        # Placeholder calculation
        df["favorite_implied_prob"] = None
        df["underdog_implied_prob"] = None
        df["market_overround"] = None
        df["is_home_favorite"] = None

        return df[["event_id"] + self.output_columns]
