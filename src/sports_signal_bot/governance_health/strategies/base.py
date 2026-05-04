from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseGovernanceHealthStrategy(ABC):
    @abstractmethod
    def evaluate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        pass
