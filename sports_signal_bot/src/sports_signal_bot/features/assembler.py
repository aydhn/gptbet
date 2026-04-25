from typing import Dict, List

import pandas as pd

from sports_signal_bot.core.logger import get_logger
from sports_signal_bot.features.contracts import NullPolicy
from sports_signal_bot.features.utils.nulls import apply_null_policy

logger = get_logger("FeatureSetAssembler")


class FeatureSetAssembler:
    """Joins output from multiple builders into a single, cohesive matrix."""

    def __init__(self):
        self.feature_dfs: Dict[str, pd.DataFrame] = {}

    def add_feature_set(self, builder_name: str, df: pd.DataFrame):
        """Registers a dataframe produced by a builder."""
        if "event_id" not in df.columns:
            logger.warning(
                f"Builder {builder_name} output missing 'event_id'. Skipping."
            )
            return

        # Ensure event_id is string and no duplicates
        df["event_id"] = df["event_id"].astype(str)
        if df["event_id"].duplicated().any():
            logger.warning(
                f"Builder {builder_name} produced duplicate event_ids. Keeping first."
            )
            df = df.drop_duplicates(subset=["event_id"], keep="first")

        self.feature_dfs[builder_name] = df

    def assemble(self, null_policy: NullPolicy = NullPolicy.KEEP_NULLS) -> pd.DataFrame:
        """Outer joins all registered feature sets on event_id."""
        if not self.feature_dfs:
            return pd.DataFrame()

        # Start with the first dataframe
        builder_names = list(self.feature_dfs.keys())
        base_df = self.feature_dfs[builder_names[0]].copy()

        for name in builder_names[1:]:
            df_to_join = self.feature_dfs[name]
            base_df = pd.merge(
                base_df,
                df_to_join,
                on="event_id",
                how="outer",
                suffixes=("", f"_{name}"),
            )

        # Apply basic null policy (more advanced null handling can go to utils/nulls.py later)
        if null_policy == NullPolicy.FILL_DEFAULTS:
            base_df = apply_null_policy(
                base_df, null_policy
            )  # Basic fill, in real prod might be column-specific

        return base_df
