from abc import ABC, abstractmethod
from typing import Any, Dict, List

from sports_signal_bot.dynamic_weighting.contracts import (
    DynamicWeightRecord, WeightingPolicyDefinition)


class BaseWeightingStrategy(ABC):
    def __init__(self, policy: WeightingPolicyDefinition, config: Dict[str, Any]):
        self.policy = policy
        self.config = config

    @abstractmethod
    def compute_weights(
        self, eligible_sources: List[Dict[str, Any]], context: Dict[str, Any]
    ) -> List[DynamicWeightRecord]:
        """Compute dynamic weights for a list of eligible sources."""
        pass

    def describe(self) -> str:
        return f"{self.__class__.__name__} using policy {self.policy.name}"

    def validate_inputs(self, eligible_sources: List[Dict[str, Any]]) -> bool:
        if not eligible_sources:
            return False
        return True
