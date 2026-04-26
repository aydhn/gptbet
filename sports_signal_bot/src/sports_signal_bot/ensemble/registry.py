from typing import Dict, Type

from .strategies.base import BaseEnsembler
from .strategies.best_source_fallback import BestSourceFallbackEnsembler
from .strategies.dynamic_weighted_average import \
    DynamicWeightedAverageEnsembler
from .strategies.reliability_weighted import ReliabilityWeightedEnsembler
from .strategies.rule_based_hybrid import RuleBasedHybridEnsembler
from .strategies.simple_average import SimpleAverageEnsembler
from .strategies.weighted_average import WeightedAverageEnsembler


class EnsembleRegistry:

    _registry: Dict[str, Type[BaseEnsembler]] = {
        "simple_average": SimpleAverageEnsembler,
        "weighted_average": WeightedAverageEnsembler,
        "dynamic_weighted_average": DynamicWeightedAverageEnsembler,
        "reliability_weighted": ReliabilityWeightedEnsembler,
        "best_source_fallback": BestSourceFallbackEnsembler,
        "rule_based_hybrid": RuleBasedHybridEnsembler,
    }

    @classmethod
    def register(cls, name: str, strategy_class: Type[BaseEnsembler]):
        cls._registry[name] = strategy_class

    @classmethod
    def get(cls, name: str) -> Type[BaseEnsembler]:
        if name not in cls._registry:
            raise ValueError(
                f"Ensemble strategy '{name}' not found. Available: {list(cls._registry.keys())}"
            )
        return cls._registry[name]

    @classmethod
    def list_available(cls) -> list[str]:
        return list(cls._registry.keys())
