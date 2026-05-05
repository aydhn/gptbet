"""
ReproducibilityFirstStrategy.
"""
from .base import BaseHardeningStrategy
from typing import Dict, Any

class ReproducibilityFirstStrategy(BaseHardeningStrategy):
    def apply(self, context: Dict[str, Any]) -> Dict[str, Any]:
        return {"strategy": "ReproducibilityFirstStrategy", "strictness": "high", "block_on_repro_fail": True}
