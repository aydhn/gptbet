from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseExternalAuditStrategy(ABC):
    @abstractmethod
    def evaluate_external_input(self, input_data: Dict[str, Any]) -> str:
        pass

    @abstractmethod
    def get_readiness_weights(self) -> Dict[str, float]:
        pass
