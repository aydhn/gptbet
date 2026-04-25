from typing import Dict, List

import pandas as pd

from sports_signal_bot.features.base import BaseFeatureBuilder
from sports_signal_bot.features.contracts import FeatureBuildContext


class BasketballSpreadEnvironmentBuilder(BaseFeatureBuilder):
    """Calculates basketball-specific spread covering proxies."""

    @property
    def name(self) -> str:
        return "basketball_spread_env"

    @property
    def family(self) -> str:
        return "score_environment"

    @property
    def supported_sports(self) -> List[str]:
        return ["basketball"]

    @property
    def required_inputs(self) -> List[str]:
        return ["events"]

    @property
    def output_columns(self) -> List[str]:
        return ["home_ats_proxy", "away_ats_proxy"]

    def build(
        self, context: FeatureBuildContext, data: Dict[str, pd.DataFrame]
    ) -> pd.DataFrame:
        events_df = data["events"]
        df = pd.DataFrame({"event_id": events_df["event_id"]})

        df["home_ats_proxy"] = 0.5
        df["away_ats_proxy"] = 0.5

        return df
