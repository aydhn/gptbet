from abc import ABC, abstractmethod
from typing import Dict, Any

class BasePerformanceHardeningStrategy(ABC):
    @abstractmethod
    def evaluate_envelope(self, target_ref: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_cache_ttl(self, family: str) -> int:
        pass
