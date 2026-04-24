import pandas as pd
from typing import Dict, List
from sports_signal_bot.features.base import BaseFeatureBuilder
from sports_signal_bot.features.contracts import FeatureBuildContext

class ContextFeatureBuilder(BaseFeatureBuilder):
    """Extracts basic context features like home/away, dates, etc."""

    @property
    def name(self) -> str:
        return "context_features"

    @property
    def family(self) -> str:
        return "identity_context"

    @property
    def supported_sports(self) -> List[str]:
        return ["all"]

    @property
    def required_inputs(self) -> List[str]:
        return ["events"]

    @property
    def output_columns(self) -> List[str]:
        return [
            "sport", "league", "season", "event_month",
            "event_weekday", "kickoff_hour", "home_indicator"
        ]

    def build(self, context: FeatureBuildContext, data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        events_df = data["events"].copy()

        # Ensure event_id exists
        if "event_id" not in events_df.columns:
            return pd.DataFrame(columns=["event_id"] + self.output_columns)

        # Parse datetime if available
        if "event_datetime_utc" in events_df.columns:
            dt = pd.to_datetime(events_df["event_datetime_utc"])
            events_df["event_month"] = dt.dt.month
            events_df["event_weekday"] = dt.dt.weekday
            events_df["kickoff_hour"] = dt.dt.hour
        else:
            events_df["event_month"] = None
            events_df["event_weekday"] = None
            events_df["kickoff_hour"] = None

        # Add placeholders/constants
        events_df["sport"] = context.sport
        events_df["league"] = events_df.get("league", None)
        events_df["season"] = events_df.get("season", None)

        # We will assume each row is represented from home perspective for simplicity in tabular form
        events_df["home_indicator"] = 1

        cols = ["event_id"] + [c for c in self.output_columns if c in events_df.columns]
        return events_df[cols]
