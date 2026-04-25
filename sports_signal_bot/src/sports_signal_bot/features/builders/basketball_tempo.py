from typing import Dict, List

import pandas as pd

from sports_signal_bot.features.base import BaseFeatureBuilder
from sports_signal_bot.features.contracts import FeatureBuildContext


class BasketballTempoBuilder(BaseFeatureBuilder):
    """Calculates basketball-specific pace and tempo proxies."""

    @property
    def name(self) -> str:
        return "basketball_tempo"

    @property
    def family(self) -> str:
        return "sport_specific"

    @property
    def supported_sports(self) -> List[str]:
        return ["basketball"]

    @property
    def required_inputs(self) -> List[str]:
        return ["events"]

    @property
    def output_columns(self) -> List[str]:
        return ["home_pace_proxy", "away_pace_proxy", "matchup_pace_projection"]

    def build(
        self, context: FeatureBuildContext, data: Dict[str, pd.DataFrame]
    ) -> pd.DataFrame:
        events_df = data["events"]
        df = pd.DataFrame({"event_id": events_df["event_id"]})

        df["home_pace_proxy"] = 100.0
        df["away_pace_proxy"] = 100.0
        df["matchup_pace_projection"] = 100.0

        return df
