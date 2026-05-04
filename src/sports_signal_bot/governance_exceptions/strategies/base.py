from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseGovernanceExceptionStrategy(ABC):

    @property
    @abstractmethod
    def strategy_name(self) -> str:
        pass

    @abstractmethod
    def evaluate(self, context: Dict[str, Any]) -> str:
        pass
