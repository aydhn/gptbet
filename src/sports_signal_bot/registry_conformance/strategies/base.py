from abc import ABC, abstractmethod
from typing import Dict, Any


class RegistryConformanceStrategy(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def apply(self, context: Dict[str, Any]) -> Dict[str, Any]:
        pass
