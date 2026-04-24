from abc import ABC, abstractmethod
import pandas as pd
from typing import List

class BaseFeatureBuilder(ABC):
    @abstractmethod
    def build_features(self, events: List[dict]) -> pd.DataFrame:
        """Transforms raw event dicts to a feature dataframe."""
        pass

class FeatureSet:
    def __init__(self, name: str, features: List[str]):
        self.name = name
        self.features = features

class FeatureRegistry:
    def __init__(self):
        self._builders = {}

    def register(self, name: str, builder: BaseFeatureBuilder):
        self._builders[name] = builder

    def get_builder(self, name: str) -> BaseFeatureBuilder:
        return self._builders.get(name)
