from abc import ABC, abstractmethod
from typing import Dict, Any, List

class CoherenceScoringStrategy(ABC):
    @abstractmethod
    def evaluate(self, inputs: List[Dict[str, Any]]) -> Dict[str, Any]:
        pass
