from typing import Dict, Any
from .registry import StackerRegistry
from .trainers.base import BaseStacker

class StackerFactory:
    @staticmethod
    def create(name: str, config: Dict[str, Any] = None) -> BaseStacker:
        if config is None:
            config = {}
        stacker_class = StackerRegistry.get(name)
        return stacker_class(config)
