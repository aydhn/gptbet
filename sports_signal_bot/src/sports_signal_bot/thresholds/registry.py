from typing import Dict, Type

from .strategies.base import BaseThresholdOptimizer


class ThresholdStrategyRegistry:
    _strategies: Dict[str, Type[BaseThresholdOptimizer]] = {}

    @classmethod
    def register(cls, name: str, strategy_class: Type[BaseThresholdOptimizer]) -> None:
        cls._strategies[name] = strategy_class

    @classmethod
    def get(cls, name: str) -> Type[BaseThresholdOptimizer]:
        if name not in cls._strategies:
            raise ValueError(f"Threshold strategy {name} not found in registry")
        return cls._strategies[name]

    @classmethod
    def list_strategies(cls) -> Dict[str, Type[BaseThresholdOptimizer]]:
        return cls._strategies.copy()
