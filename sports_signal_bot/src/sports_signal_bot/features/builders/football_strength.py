from typing import Dict, List

import pandas as pd

from sports_signal_bot.features.base import BaseFeatureBuilder
from sports_signal_bot.features.contracts import FeatureBuildContext


class FootballTeamStrengthBuilder(BaseFeatureBuilder):
    """Calculates football-specific team strength proxies."""

    @property
    def name(self) -> str:
        return "football_team_strength"

    @property
    def family(self) -> str:
        return "team_strength"

    @property
    def supported_sports(self) -> List[str]:
        return ["football"]

    @property
    def required_inputs(self) -> List[str]:
        return ["events"]

    @property
    def output_columns(self) -> List[str]:
        return ["home_rating_proxy", "away_rating_proxy", "rating_diff"]

    def build(
        self, context: FeatureBuildContext, data: Dict[str, pd.DataFrame]
    ) -> pd.DataFrame:
        events_df = data["events"]
        df = pd.DataFrame({"event_id": events_df["event_id"]})

        df["home_rating_proxy"] = 1500.0
        df["away_rating_proxy"] = 1500.0
        df["rating_diff"] = 0.0

        return df
