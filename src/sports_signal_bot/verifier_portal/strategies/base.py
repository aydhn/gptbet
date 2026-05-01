from typing import Dict, Any, List
from abc import ABC, abstractmethod

class VerifierPortalStrategy(ABC):
    @abstractmethod
    def apply_strategy(self) -> Dict[str, Any]:
        pass
