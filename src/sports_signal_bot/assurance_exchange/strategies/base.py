from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseAssuranceExchangeStrategy(ABC):
    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_quarantine_default(self) -> bool:
        pass

    @abstractmethod
    def evaluate_acceptance(self, packet_id: str, context: Dict[str, Any]) -> str:
        pass
