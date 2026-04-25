from abc import ABC, abstractmethod
from typing import Any, Dict, List, Type

import pandas as pd

from sports_signal_bot.features.contracts import FeatureBuildContext


class BaseFeatureBuilder(ABC):
    """Abstract base class for all feature builders."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the feature builder."""
        pass

    @property
    @abstractmethod
    def family(self) -> str:
        """Family this feature belongs to (e.g., 'context', 'team_strength')."""
        pass

    @property
    @abstractmethod
    def supported_sports(self) -> List[str]:
        """List of supported sports, e.g., ['football', 'basketball'] or ['all']."""
        pass

    @property
    @abstractmethod
    def required_inputs(self) -> List[str]:
        """List of required input data sources, e.g., ['events', 'odds']."""
        pass

    @property
    @abstractmethod
    def output_columns(self) -> List[str]:
        """List of column names this builder is expected to produce."""
        pass

    @abstractmethod
    def build(
        self, context: FeatureBuildContext, data: Dict[str, pd.DataFrame]
    ) -> pd.DataFrame:
        """
        Builds the features given the context and input datasets.
        Returns a DataFrame containing 'event_id' and the generated feature columns.
        """
        pass
