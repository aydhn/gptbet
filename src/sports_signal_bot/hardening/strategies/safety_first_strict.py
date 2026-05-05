"""
SafetyFirstStrictStrategy.
"""
from .base import BaseHardeningStrategy
from typing import Dict, Any

class SafetyFirstStrictStrategy(BaseHardeningStrategy):
    def apply(self, context: Dict[str, Any]) -> Dict[str, Any]:
        return {"strategy": "SafetyFirstStrictStrategy", "strictness": "highest", "block_on_safety_critical": True}
