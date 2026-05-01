from abc import ABC, abstractmethod
from typing import Dict, Any
from ..contracts import RunMode

class BaseConformanceStrategy(ABC):
    @abstractmethod
    def apply_strategy(self, state: Dict[str, Any], mode: RunMode) -> Dict[str, Any]:
        pass
