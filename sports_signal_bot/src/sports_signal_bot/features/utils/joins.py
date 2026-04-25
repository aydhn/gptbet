from typing import Optional

import pandas as pd

from sports_signal_bot.core.logger import get_logger

logger = get_logger("JoinUtils")


def safe_merge(
    left: pd.DataFrame,
    right: pd.DataFrame,
    on: str,
    how: str = "left",
    validate: Optional[str] = None,
) -> pd.DataFrame:
    """
    Safely merges two dataframes, logging warnings if row counts change unexpectedly.
    """
    initial_rows = len(left)
    merged = pd.merge(left, right, on=on, how=how, validate=validate)
    final_rows = len(merged)

    if final_rows != initial_rows and how in ["left", "inner"]:
        logger.warning(
            f"Row count changed during '{how}' merge on '{on}'. Initial: {initial_rows}, Final: {final_rows}"
        )

    return merged
