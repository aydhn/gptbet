from typing import Dict, Type, Any
from .trainers.base import BaseStacker

class StackerRegistry:
    _registry: Dict[str, Type[BaseStacker]] = {}

    @classmethod
    def register(cls, name: str):
        def wrapper(stacker_cls: Type[BaseStacker]):
            cls._registry[name] = stacker_cls
            return stacker_cls
        return wrapper

    @classmethod
    def get(cls, name: str) -> Type[BaseStacker]:
        if name not in cls._registry:
            raise ValueError(f"Stacker model '{name}' is not registered.")
        return cls._registry[name]

    @classmethod
    def list_stackers(cls) -> list[str]:
        return list(cls._registry.keys())

# Register built-in stackers
from .trainers.logistic import MetaLogisticStacker
from .trainers.gradient_boosting import MetaGradientBoostingStacker
from .trainers.identity import MetaIdentityStacker

StackerRegistry.register("meta_logistic")(MetaLogisticStacker)
StackerRegistry.register("meta_gradient_boosting")(MetaGradientBoostingStacker)
StackerRegistry.register("identity")(MetaIdentityStacker)
