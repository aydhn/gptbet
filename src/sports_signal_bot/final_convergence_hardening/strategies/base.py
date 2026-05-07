from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseFinalConvergenceStrategy(ABC):
    @abstractmethod
    def evaluate(self, convergence_data: Dict[str, Any]) -> bool:
        pass
