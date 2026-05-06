from abc import ABC, abstractmethod
from typing import Dict, Any

class EnduranceHardeningStrategy(ABC):
    @abstractmethod
    def evaluate_endurance(self, telemetry: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @property
    @abstractmethod
    def strategy_name(self) -> str:
        pass
