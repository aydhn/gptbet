from typing import Dict, Any
from .base import TransparencyStrategy

class ConservativeTransparencyStrategy(TransparencyStrategy):
    def enforce_policy(self, event_context: Dict[str, Any]) -> bool:
        # Strict critical log coverage required, missing signature blocks it
        is_critical = event_context.get("is_critical", False)
        has_signature = event_context.get("has_signature", False)
        if is_critical and not has_signature:
            return False
        return True
