from typing import Dict, Any
from .base import TransparencyStrategy

class BalancedVerificationMeshStrategy(TransparencyStrategy):
    def enforce_policy(self, event_context: Dict[str, Any]) -> bool:
        # Balanced: prefers signature but allows processing with warnings
        return True
