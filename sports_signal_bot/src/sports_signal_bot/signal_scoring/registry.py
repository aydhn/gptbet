from typing import Dict, Type
from sports_signal_bot.signal_scoring.strategies.base import BaseSignalScorer

class SignalScorerRegistry:

    _strategies: Dict[str, Type[BaseSignalScorer]] = {}

    @classmethod
    def register(cls, name: str, strategy_class: Type[BaseSignalScorer]) -> None:
        cls._strategies[name] = strategy_class

    @classmethod
    def get(cls, name: str) -> Type[BaseSignalScorer]:
        if name not in cls._strategies:
            raise ValueError(f"Unknown signal scoring strategy: {name}")
        return cls._strategies[name]

    @classmethod
    def list_strategies(cls) -> Dict[str, Type[BaseSignalScorer]]:
        return cls._strategies.copy()
