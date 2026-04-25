from typing import Any, Dict, List

import pandas as pd

from sports_signal_bot.core.logger import get_logger
from sports_signal_bot.features.base import BaseFeatureBuilder
from sports_signal_bot.features.contracts import FeatureBuildContext
from sports_signal_bot.ratings.contracts import RatingSnapshotRecord

logger = get_logger(__name__)


class RatingFeatureBuilder(BaseFeatureBuilder):
    @property
    def name(self) -> str:
        return "rating_features"

    @property
    def family(self) -> str:
        return "strength"

    @property
    def supported_sports(self) -> List[str]:
        return ["all"]

    @property
    def required_inputs(self) -> List[str]:
        return ["events", "rating_snapshots"]

    @property
    def output_columns(self) -> List[str]:
        return [
            "rating_home_pre",
            "rating_away_pre",
            "rating_diff",
            "rating_abs_diff",
            "rating_exp_home_win",
        ]

    def build(
        self, context: FeatureBuildContext, data: Dict[str, pd.DataFrame]
    ) -> pd.DataFrame:
        events_df = data.get("events")
        if events_df is None or events_df.empty:
            return pd.DataFrame()

        snapshots = data.get("rating_snapshots")
        if not snapshots:
            df = pd.DataFrame(events_df["event_id"])
            for col in [
                "rating_home_pre",
                "rating_away_pre",
                "rating_diff",
                "rating_abs_diff",
                "rating_exp_home_win",
            ]:
                df[col] = None
            return df.set_index("event_id")

        snap_df = (
            pd.DataFrame([s.model_dump() for s in snapshots])
            if isinstance(snapshots, list)
            else snapshots
        )
        features = []
        for _, row in snap_df.iterrows():
            diff = (
                row["pre_home_rating"]
                + row.get("home_advantage_applied", 0.0)
                - row["pre_away_rating"]
            )
            features.append(
                {
                    "event_id": row["event_id"],
                    "rating_home_pre": row["pre_home_rating"],
                    "rating_away_pre": row["pre_away_rating"],
                    "rating_diff": diff,
                    "rating_abs_diff": abs(diff),
                    "rating_exp_home_win": row["expected_home_score"],
                }
            )

        result = pd.merge(
            events_df[["event_id"]], pd.DataFrame(features), on="event_id", how="left"
        )
        return result.set_index("event_id")
