from abc import ABC, abstractmethod
from typing import Dict, Any

class TransparencyStrategy(ABC):
    @abstractmethod
    def enforce_policy(self, event_context: Dict[str, Any]) -> bool:
        """Evaluate transparency policy based on strategy."""
        pass
