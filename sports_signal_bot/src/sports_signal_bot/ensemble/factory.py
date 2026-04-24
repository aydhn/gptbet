from typing import Dict, Any
from .registry import EnsembleRegistry
from .strategies.base import BaseEnsembler

class EnsembleFactory:

    @staticmethod
    def create(name: str, config: Dict[str, Any] = None) -> BaseEnsembler:
        strategy_class = EnsembleRegistry.get(name)
        return strategy_class(name=name, config=config or {})
