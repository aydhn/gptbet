import pandas as pd
from typing import Dict, List
from sports_signal_bot.features.base import BaseFeatureBuilder
from sports_signal_bot.features.contracts import FeatureBuildContext

class FootballGoalEnvironmentBuilder(BaseFeatureBuilder):
    """Calculates football-specific goal scoring environment proxies."""

    @property
    def name(self) -> str:
        return "football_goal_env"

    @property
    def family(self) -> str:
        return "score_environment"

    @property
    def supported_sports(self) -> List[str]:
        return ["football"]

    @property
    def required_inputs(self) -> List[str]:
        return ["events"]

    @property
    def output_columns(self) -> List[str]:
        return [
            "expected_total_placeholder", "home_team_total_proxy", "away_team_total_proxy"
        ]

    def build(self, context: FeatureBuildContext, data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        events_df = data["events"]
        df = pd.DataFrame({"event_id": events_df["event_id"]})

        df["expected_total_placeholder"] = 2.5
        df["home_team_total_proxy"] = 1.3
        df["away_team_total_proxy"] = 1.2

        return df
