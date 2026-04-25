from abc import ABC, abstractmethod
from typing import Any, Dict, Generator, List, Tuple

import numpy as np
import pandas as pd

from sports_signal_bot.core.logger import get_logger

logger = get_logger("SplitStrategies")


class BaseSplitStrategy(ABC):
    """Abstract base class for all time-aware split strategies."""

    @abstractmethod
    def split(
        self, df: pd.DataFrame, datetime_col: str = "event_datetime_utc"
    ) -> Generator[Tuple[str, np.ndarray, np.ndarray, np.ndarray], None, None]:
        """
        Yields fold_id, train_indices, valid_indices, test_indices (optional)
        """
        pass


class HoldoutTimeSplit(BaseSplitStrategy):
    """Simple chronological train/valid/test split based on cutoff dates or fractions."""

    def __init__(self, train_fraction: float = 0.8, test_fraction: float = 0.0):
        self.train_fraction = train_fraction
        self.test_fraction = test_fraction
        self.valid_fraction = 1.0 - train_fraction - test_fraction

    def split(
        self, df: pd.DataFrame, datetime_col: str = "event_datetime_utc"
    ) -> Generator[Tuple[str, np.ndarray, np.ndarray, np.ndarray], None, None]:
        if df.empty:
            return

        # Ensure sorted
        if not df[datetime_col].is_monotonic_increasing:
            df = df.sort_values(datetime_col)

        n = len(df)
        train_end = int(n * self.train_fraction)
        valid_end = int(n * (self.train_fraction + self.valid_fraction))

        indices = df.index.values
        train_idx = indices[:train_end]
        valid_idx = indices[train_end:valid_end]
        test_idx = indices[valid_end:] if self.test_fraction > 0 else np.array([])

        yield "holdout_1", train_idx, valid_idx, test_idx


class ExpandingWindowSplit(BaseSplitStrategy):
    """Expanding train window, fixed-size valid window. Time-based (e.g. months) or row-based."""

    def __init__(self, initial_train_size: int, valid_size: int, step_size: int = None):
        self.initial_train_size = initial_train_size
        self.valid_size = valid_size
        self.step_size = step_size or valid_size

    def split(
        self, df: pd.DataFrame, datetime_col: str = "event_datetime_utc"
    ) -> Generator[Tuple[str, np.ndarray, np.ndarray, np.ndarray], None, None]:
        if df.empty:
            return

        n = len(df)
        indices = df.index.values

        start = 0
        train_end = self.initial_train_size
        fold = 1

        while train_end < n:
            valid_end = min(n, train_end + self.valid_size)

            train_idx = indices[start:train_end]
            valid_idx = indices[train_end:valid_end]

            yield f"expanding_{fold}", train_idx, valid_idx, np.array([])

            train_end += self.step_size
            fold += 1


class RollingWindowSplit(BaseSplitStrategy):
    """Fixed-size rolling train window, fixed-size valid window."""

    def __init__(self, train_size: int, valid_size: int, step_size: int = None):
        self.train_size = train_size
        self.valid_size = valid_size
        self.step_size = step_size or valid_size

    def split(
        self, df: pd.DataFrame, datetime_col: str = "event_datetime_utc"
    ) -> Generator[Tuple[str, np.ndarray, np.ndarray, np.ndarray], None, None]:
        if df.empty:
            return

        n = len(df)
        indices = df.index.values

        train_start = 0
        train_end = self.train_size
        fold = 1

        while train_end < n:
            valid_end = min(n, train_end + self.valid_size)

            train_idx = indices[train_start:train_end]
            valid_idx = indices[train_end:valid_end]

            yield f"rolling_{fold}", train_idx, valid_idx, np.array([])

            train_start += self.step_size
            train_end += self.step_size
            fold += 1


class WalkForwardSplit(ExpandingWindowSplit):
    """Alias for ExpandingWindowSplit in many contexts, but can be customized."""

    pass
