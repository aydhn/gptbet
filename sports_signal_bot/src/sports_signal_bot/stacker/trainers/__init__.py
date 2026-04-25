from .base import BaseStacker
from .logistic import MetaLogisticStacker
from .gradient_boosting import MetaGradientBoostingStacker
from .identity import MetaIdentityStacker

__all__ = [
    "BaseStacker",
    "MetaLogisticStacker",
    "MetaGradientBoostingStacker",
    "MetaIdentityStacker"
]
