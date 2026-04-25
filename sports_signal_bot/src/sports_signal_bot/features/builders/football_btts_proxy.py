from typing import Dict, List

import pandas as pd

from sports_signal_bot.features.base import BaseFeatureBuilder
from sports_signal_bot.features.contracts import FeatureBuildContext


class FootballBTTSProxyBuilder(BaseFeatureBuilder):
    """Calculates Both Teams To Score (BTTS) rate proxies."""

    @property
    def name(self) -> str:
        return "football_btts_proxy"

    @property
    def family(self) -> str:
        return "sport_specific"

    @property
    def supported_sports(self) -> List[str]:
        return ["football"]

    @property
    def required_inputs(self) -> List[str]:
        return ["events"]

    @property
    def output_columns(self) -> List[str]:
        return ["home_btts_rate_proxy", "away_btts_rate_proxy", "combined_btts_proxy"]

    def build(
        self, context: FeatureBuildContext, data: Dict[str, pd.DataFrame]
    ) -> pd.DataFrame:
        events_df = data["events"]
        df = pd.DataFrame({"event_id": events_df["event_id"]})

        df["home_btts_rate_proxy"] = 0.5
        df["away_btts_rate_proxy"] = 0.5
        df["combined_btts_proxy"] = 0.5

        return df
